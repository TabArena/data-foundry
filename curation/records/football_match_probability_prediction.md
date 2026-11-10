---
unique_name: football_match_probability_prediction
name: Football Match Probability Prediction (Kaggle community competition, Octosport with Sportmonks data)
checked_by:
- Myunghwan
data_foundry_status:
- 'DF: Suspended'
suggestion: TBD -> 2nd Tier
priority: 4
tags:
- Non-IID (Temporal)
- Revisit later
original_source: Kaggle
year: '2022'
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/football-match-probability-prediction
- https://www.sportmonks.com/blogs/football-predictions-kaggle-competition
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: a competition on over 150,000 matches of more than 860 leagues, with pre-match features only, the bookmakers' probabilities as the benchmark and log loss as the metric; the organisers acknowledged a date leak through the history columns, which a temporal split handles.
- Source: Kaggle community competition "Football Match Probability Prediction" by Octosport and Sportmonks, 2022-02-07 to 2022-05-06, 381 teams (Kaggle API). As published: train.csv (180 MB, with `target`), test.csv (118 MB, no target), train_target_and_scores.csv (the final scores), sample_submission.csv; "more than 150000 historical world football matches from 2019 to 2021, with more than 860 leagues and 9500 teams"; descriptive columns (match date, league, `is_cup`, coach ids; team names hidden in test) and, for each team, its 10 previous matches (date, home or away, goals, Octosport ratings, league, coach) (data-description page). Rows per file not counted.
- Source's words: "Do you want to beat the bookmaker's performance? ... we also added the performance of the bookmakers as a benchmark. We turned their odds into probabilities" (Description); the team ratings are not given for the predicted match: "The reason being these ratings will already contain the winning probabilities information" (organiser, discussion 314078).
- Use case: a bettor or a bookmaker setting the probabilities of home win, draw and away win before kick-off; fit direct. Regime temporal: "Both the train and test sets are time-ordered so CV should be done carefully" (organiser, discussion 314744); teams as groups inside.
- Siblings and duplicates: `laduma_analytics_football_league_winners_prediction_challenge` and `zindi_weekendz_laduma_analytics_football_league_winners_prediction_challenge` (AI `TBD -> 2nd Tier`, priority 1; one masked African league, a few hundred games, in-match statistics); `open_international_soccer_database` (a run candidate: 216,743 matches of 52 leagues, 2000-2017, results only, scored by RPS); `sports_bet_datasets` (a review's source list). Other sources, not duplicates (PROV-4). External collections: none found.
- Better data: found as better data for `laduma_analytics_football_league_winners_prediction_challenge`, `zindi_weekendz_laduma_analytics_football_league_winners_prediction_challenge`; no further search this round.
- Papers and pages: the competition pages; the winners used LSTM ensembles and a single LSTM, and "Almost all solutions on the top leaderboard have been forked or derived from the LSTM starter" (organiser, discussion 324277).
- Metric: multinomial log loss over home, draw and away (Evaluation page; Kaggle API `Multiclass Loss`), the leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: the date leak: "since we decided to provide Sportsmonk ids, data-leakage is easy"; "About the date leak : we were aware of it" (organiser, discussion 314744): a match's result appears in the history columns of later matches, so the split must be temporal and later rows must not feed earlier ones (LEAK, SPLIT-6); only train.csv has labels, so the data is train.csv alone; the wide history block (10 matches x 2 teams x several fields) suited sequence models in the competition; team and coach ids.
- Priority: gap + (multiclass thin), use case + (the bookmakers' probabilities named as the benchmark), source + (a documented data page, the organisers' answers), shape + (most of the 150,000 matches labelled, wide mixed columns, temporal), risk - (the acknowledged date leak).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `laduma_analytics_football_league_winners_prediction_challenge`, `zindi_weekendz_laduma_analytics_football_league_winners_prediction_challenge`.
- as published: Matches as units; 'more than 150,000 historical matches from 2019 to 2021, more than 860 leagues and 9,500 teams' (Sportmonks); files train.csv (180 MB), test.csv (118 MB), ...; target: Match outcome home / draw / away, scored as probabilities with multiclass log loss (the leaderboard metric); access: registration.
- Why: The same target (home win / draw / away) and the same leaderboard metric (log loss) as the Laduma rerun, with features of the same kind (team and match history), and here the per-row history covers only matches before the one predicted, so the in-match leak the Laduma records carry is avoided by construction.
- Adds: Hundreds of times more matches (over 150,000 against a few hundred), hundreds of leagues instead of one masked league, pre-match features only. Note: the Open International Soccer Database (Dubitzky et al., Machine Learning 108, 2019; 216,743 matches, 52 leagues, 2000-2017; results only) is a second source of the ...

CC (2026-11-09, Myunghwan): Defer Football Match Probability Prediction: "The difference seems weak. We may want to defer this dataset." Record this decision in the draft PR. This is a hold on pursuing inclusion, not a scientific rejection.

**Assessment (AI, 2026-11-09, curator deferral):** Save this as a candidate-specific second-tier hold for weak demonstrated incremental model value. In the bounded 18-fit study, January-selected engineered LightGBM averaged source multinomial log loss 1.018451 versus strict raw logistic regression 1.023423: a small 0.004973 (0.486%) improvement, winning February/April and losing March. The best tested smoothed home/away team-record heuristic scored 1.056243. Engineered logistic averaged 1.023029, with iteration caps in April/March; no optimized-linear or exhaustive advanced-family claim follows. The small measured signal is retained; no Trivial, Too Small, No Signal or general minimum-gain rule is inferred. The source-defined fixture task and previously chosen ordinary temporal splits remain valid as qualified; this hold does not reopen that choice or establish a new leak. Preserve the exploratory definition, source files, predictions and independent audits locally. Suspend inclusion/build and release only this active reservation through the official workflow. Suggested reopening guidance: an explicit curator request supported by a justified task/model revision or stronger appropriately validated incremental-value evidence; this guidance is an AI suggestion, not a new quoted curator condition or authorization for unattended search.
