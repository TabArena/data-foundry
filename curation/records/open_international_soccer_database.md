---
unique_name: open_international_soccer_database
name: The Open International Soccer Database for machine learning (2017 Soccer Prediction Challenge)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: Other
year: '2017'
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1007/s10994-018-5726-0
- https://osf.io/kqcye/
- https://osf.io/ftuva/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and previews of the published tables, NOT from a built dataset. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the Open International Soccer Database (Dubitzky, Lopes, Davis, Berrar; Machine Learning 2019), 216,743 league matches of 52 leagues in 35 countries from 2000 to 2017, with the 2017 Soccer Prediction Challenge's ranked probability score; a real pre-match task with a fixed metric, but the table holds only season, league, date, teams and goals, so every pre-match feature has to be built from earlier results.
- Source: the OSF project "Open International Soccer Database" (https://osf.io/kqcye/, created 2017-06-16; ISDBv1.0.txt and ISDBv2.0.txt, about 12 MB each, tab-separated) and the challenge project (https://osf.io/ftuva/); paper Dubitzky et al., "The Open International Soccer Database for machine learning", Machine Learning 108:9-28 (2019, online 2018-07-10, doi:10.1007/s10994-018-5726-0). The record's link osf.io/kgcve was an OSF user page, not the data, and is replaced. As published (paper, Sec. 3): "Each entry in the Database is described by the nine fields" Sea, Lge, Date, HT, AT, HS, AS, GD, WDL (home win, draw, away win); "results of 216,743 games played between 19/03/2000 and 21/03/2017 from 52 leagues in 35 countries"; the challenge's prediction set holds 206 matches from 31 March 2017. The v2.0 file preview has the same nine columns.
- Use case: the paper poses "a real-world machine learning problem with a fixed time line and a genuine prediction task: to develop a predictive model from the Database and then to predict the outcome of the 206 future soccer matches" (Abstract); who acts on it (a bookmaker or bettor before kick-off) is not named, so the fit is approximate. Regime temporal (the challenge predicted matches after the learning set), with teams recurring inside.
- Siblings and duplicates: `football_match_probability_prediction` (Kaggle 2022, more than 150,000 matches of 2019-2021 with each team's last ten matches as features; `TBD -> Yes`, priority 4) is the same task with pre-match features shipped; `sports_bet_datasets` (`TBD -> 2nd Tier`, priority 1) is the review's list of sources that names this database. External collections: none found.
- Better data: found as better data for `sports_bet_datasets`; no further search this round.
- Papers and pages: the paper above. Sec. 5, Table 8: the winner, Team OH, scored an average RPS of 0.2063 (Hubáček, Šourek and Železný, "Learning to predict soccer results from relational data with gradient boosted trees", Machine Learning 108:29-47, doi:10.1007/s10994-018-5704-6, moved here from the links); the organisers' out-of-competition entry 0.2054 (Berrar, Lopes and Dubitzky, "Incorporating domain knowledge in machine learning for soccer outcome prediction", doi:10.1007/s10994-018-5747-8); the global and league priors 0.2261 and 0.2255. Neither method paper was read.
- Metric: the ranked probability score averaged over matches, the challenge's ranking criterion (paper Sec. 4.2, Eq. 1 and 2: "The goal of the Challenge was to minimize the average over all ranked probability scores"); a competition's deliberate choice (MET-4); inputs: the outcome order W, D, L only. Not a standard scikit-learn metric, so a reference implementation ships with the dataset (MET-13).
- Risks for /add-dataset: HS, AS and GD are the match's own result and go (LEAK-10); ratings, recent form and goal differences must be derived from each team's earlier matches only, a construction of ours rather than the source's (`Needs extensive data wrangling`); the forecasting-like panel test (TP-10: does a model beat each team's naive profile); "some league/season blocks are missing because of data quality issues" (Sec. 3).
- Priority: gap + (multiclass is thin), use case 0 (no actor named), source + (a paper and OSF), shape 0 (216k matches but nine raw fields, no pre-match features as published), risk - (every feature to be constructed; a sibling ships the same task with features).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `sports_bet_datasets`.
- as published: 216,743 matches, 52 leagues in 35 countries, 2000-03-19 to 2017-03-21; the challenge test set is 206 future fixtures; target: match outcome, home win / draw / away win (the challenge scored a probability over the three); access: open.
- Why: the one concrete, traceable dataset behind the review the sports_bet_datasets record points at (its own screening already named it as worth a record); a real pre-match decision, a temporal regime, and a metric the source fixed (ranked probability score)
- Adds: replaces a list of scraped sites with a single published table under one DOI: 216k matches over 17 years, a defined target, a fixed test set and a competition metric with published baselines (Hubacek et al. 2019, Berrar et al. 2019). Caveat for the add stage: the published table carries match facts only (date, ...
