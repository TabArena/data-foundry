---
unique_name: pover_t_tests_household_poverty
name: 'Pover-T Tests: Predicting Poverty (World Bank, DrivenData)'
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 2
decision_markers:
- Anonymized
tags:
- AI-Filled (Verify)
original_source: Other
domain: social science
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.drivendata.org/competitions/50/worldbank-poverty-prediction/
- https://www.drivendata.org/competitions/50/worldbank-poverty-prediction/page/99/
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-08):** `TBD -> Yes`, priority 2: the World Bank's DrivenData competition (2017-18) on whether a household is below the poverty line, from obfuscated survey answers of three unnamed countries (8,203, 3,255 and 6,469 labelled households with 344, 441 and 163 items, plus member files), scored by log loss; more households than `costa_rica_household_poverty`, but what a column asks cannot be checked.
- Source: The World Bank on DrivenData, "Pover-T Tests: Predicting Poverty" (competition 50; the host's benchmark post of 2017-12-19 already uses the data; "Completed feb 2018", 2,308 joined, USD 15,000). As published (problem description page): per country A, B and C a household file and an individual file for train and test, joined by `id` (individuals by `id` and `iid`); "The training features are survey data from three countries", each column "corresponds with a survey question", multiple choice "encoded as random strings" or numeric; target `poor` in the household files; the benchmark post prints the training households as 8,203 x 344, 3,255 x 441 and 6,469 x 163 features (test 4,041, 1,604 and 3,187 households without labels), A "well-balanced", B and C "quite unbalanced", and calls it "obfuscated data from surveys conducted by The World Bank".
- The task's table: one per country, the households with their items plus aggregates of the member file; country A, 8,203 x 344 (plus the member aggregates), is the largest and the balanced one; the countries share no columns. Access: a DrivenData login and the rules ("must use the Data solely for the purpose and duration of the Competition", noted only, EV-4); whether the closed competition still serves the files is to check.
- Use case: a statistics office or the World Bank measures household poverty with a short questionnaire instead of a full consumption survey ("we can run surveys with fewer, more targeted questions that rapidly and cheaply measure the effectiveness of new policies and interventions", README of the winners' repository); fit approximate: with every question hidden it cannot be checked that the items are a short survey's and not the consumption module `poor` is computed from. Regime IID over households (one survey sample per country; no clusters published).
- Siblings and duplicates: `costa_rica_household_poverty` (`TBD -> Yes`, 3; the IDB on Kaggle, about 3,000 Costa Rican households, four levels, named columns): another source and country, no duplicate (PROV-4); `economic_well_being_prediction_challenge` (`TBD -> Yes`, a wealth index of survey clusters). grep: poverty, pover, drivendata, proxy means. External collections: none found.
- Better data: none searched (found by the data-scouting run of 2026-11-08, as better data for `costa_rica_household_poverty`); in passing, the World Bank's Poverty Prediction Challenge on DrivenData (November 2025 to February 2026: per-capita household consumption and poverty rates across survey rounds of anonymised countries; whether its data are public is not stated), worldbank.org/en/topic/measuringpoverty/brief/poverty-prediction-challenge.
- Papers and pages: the problem description and the benchmark post (blog.drivendata.org, 2017-12-19); winning solutions at github.com/drivendataorg/pover-t-tests (Ag100, private log loss 0.14797).
- Metric: "log loss scores are generated for each country, and the mean of those scores will be your overall score" (problem description), a competition's metric (MET-4): `log_loss` per country table; inputs none.
- Risks for /add-dataset: `Anonymized`: names hidden, answers recoded as random strings, countries unnamed (LEAK-32), so consumption items that compute `poor` may sit among the features (SEL-5, cannot be checked); three tables with different columns (one dataset per country, or country A only); member files to aggregate per household; only training labels were published; survey weights not mentioned.
- Priority: gap + (social science thin), use case 0 (named by the host, the fit approximate), source 0 (a competition page, no codebook, the surveys unnamed), shape + (8,203 households x 344 in country A, categorical and numeric, member tables), risk - (obfuscated columns, three different tables).

Found by the data-scouting run of 2026-11-08 for the large-datasets review (wide tables outside biology and medicine, and tables with 2M+ rows).

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates, round 2 (wide tables outside biology and medicine, tables with 2M+ rows).

**Assessment (AI, 2026-11-09):** not built in the large-datasets run of 2026-11-08: the data sits on DrivenData behind a login and the competition's terms, which this machine cannot pass. A person has to download the raw files; the build follows in a later round.

CC (2026-11-09, Lennart): later; make this its own task with a human in the loop (the data needs a person to fetch it).
