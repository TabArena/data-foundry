---
unique_name: aaia16_coal_mine_seismic_hazard
name: 'AAIA''16 Data Mining Challenge: Predicting Dangerous Seismic Events in Active Coal Mines'
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: TBD -> Yes
priority: 4
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: Other
year: '2015'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.15439/2016F560
- https://knowledgepit.ai/aaia16-data-mining-challenge/
- https://annals-csis.org/Volume_8/pliks/560.pdf
- https://doi.org/10.15439/2016F21
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: a 2015-16 competition on the task of the retired `seismic_bumps` (a dangerous seismic energy level in the next 8 hours at a longwall), with 133,151 labelled windows from 24 working sites over five years, a time-based split and AUC fixed by the organisers.
- Source: AAIA'16 Data Mining Challenge "Predicting Dangerous Seismic Events in Active Coal Mines" on Knowledge Pit (data released 2015-10-05, run to 2016-02-27), organised by Janusz and Ślęzak (University of Warsaw) with Sikora and Wróbel (Silesian University of Technology, EMAG) in the DISESOR project; summary paper in FedCSIS 2016, ACSIS vol. 8, pp. 205-211 (doi 10.15439/2016F560, read in full). As published (Sec. II): "Each case in the data was described by a series of hourly aggregated sensor readings from a 24 hour period", plus recent mining activity and "the latest assessments of the safety conditions made by mining experts", and per-site metadata (mine, region, height); "541 main attributes and 6 additional features"; training 133,151 overlapping windows from 2010-05-05 to 2014-03-06 (2.26% warnings), test 3,860 non-overlapping windows from 2014-03-07 to 2015-06-24 (5.08%), 24 working sites (Table I). Files: trainingData and four additional training parts, trainingLabels, testData, working_site_metadata (Knowledge Pit page).
- Use case: the safety staff of a longwall decide whether to raise the seismic hazard level for the coming shift, from the last 24 hours of geophone readings and the latest expert assessment (Sec. I: decision support "for predicting seismic activity in the nearest future" to protect miners); fit direct; regime temporal, because the organisers split by time stamps and the use case predicts forward; new working sites appear in the test (the cold start of Sec. IV), so the working site is grouped structure inside the temporal task (SPLIT-13).
- Siblings and duplicates: `seismic_bumps` (UCI 2013, one mine, 2,584 shifts, threshold 10^4 J; `No (Retired)`, too small as a temporal task, CC 2026-09-30) comes from the same research group and task but is another release (threshold 5*10^4 J here, 24 sites, hourly data): its own record, not a duplicate (PROV-4). No other record of the challenge (grep: aaia, knowledgepit, seismic). External collections: none found.
- Better data: found as better data for `seismic_bumps`; no further search this round.
- Papers and pages: the summary paper above; Boullé, "Predicting Dangerous Seismic Events in Coal Mines under Distribution Drift", FedCSIS 2016 (doi 10.15439/2016F21, final AUC 0.9246); the deepsense.ai write-up of the second-placed team (deepsense.ai/machine-learning-models-predicting-dangerous-seismic-events). Winner tadeusz 0.9393 final AUC; a logistic regression on the two expert-assessment columns scores 0.9196 (Table III), so the experts' assessment is a strong baseline.
- Metric: ROC AUC, the competition's leaderboard metric ("Quality of the submissions was measured using Area Under the ROC Curve (AUC)", Sec. II.A; the Knowledge Pit page says the same); deliberate (MET-4); inputs none. Declare `roc_auc`.
- Risks for /add-dataset: training windows overlap ("overlapping for consecutive cases"), so a later window's hourly energy readings contain an earlier window's target period: never an IID split, and drop the training rows whose 8-hour horizon reaches into a test window (SPLIT-9, LEAK-12). Whether the test labels were released after the challenge is unknown (the page needs a login and enrolment); without them the windows come from the 2010-2014 training data only. The 24 hourly values per measure make the table a vectorized series: check that a model on the features beats each site's naive profile (SEL-11, TP-10), and the `Time-series (Classification)` question (SEL-12). Terms: "free to use for non-commercial purposes" (noted only, EV-4).
- Priority: gap 0 (industry & manufacturing, binary and temporal not thin), use case +, source +, shape + (133,151 windows, 547 columns, 24 sites over five years), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `seismic_bumps`.
- as published: Rows = 24-hour windows of hourly aggregated geophone/seismic and mining-activity readings at one longwall working site: 133,151 training rows (overlapping windows, 2010-05-05 to 2014-03-06; main ...; target: Warning: total seismic energy released at the site in the next 8 hours exceeds 5*10^4 J (binary; 2.3% positive in training, 5.1% in test); scored by ROC AUC; access: registration.
- Why: Same target as seismic_bumps (a bump above an energy threshold in the next 8-hour shift at a longwall), same use case and the same kind of features (aggregated seismic energy and pulse counts, mining activity, hazard assessments known at the prediction point); from the same research group (Sikora, Wrobel) as the UCI ...
- Adds: About 50x more rows, 24 working sites instead of 2 longwalls, five years, a published time-based train/test split with a fixed metric (AUC); the test spans 16 months with about 196 positives against 49 in the retired record's newest half, so a temporal evaluation becomes possible. Risks: training windows overlap ...

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: 133,151 overlapping training windows and 3,860 non-overlapping test windows x 547 columns, which hold 12 period values, 22 hourly measures over 24 hours (528 columns) and 6 site fields, about 40 distinct measures; the test labels were published after the challenge, so the organisers' temporal split can be built; the call stands, priority 4.
- As published: Knowledge Pit page (https://knowledgepit.ai/aaia16-data-mining-challenge/, read 2026-11-08): "There is a total number of 541 columns in the data (including the main working site id)"; "The first part consists of an identifier of the main working site and 12 other characteristics" for the whole 24 hours; "The second part is composed of hourly aggregated measurements", 24 values per characteristic. So 541 - 13 = 528 = 22 measures x 24 hours (computed; no source states the 22). Files: trainingData.csv with trainingLabels.csv (trainingData.7z, "79,893 records"), additional_training_data_1 to 4 (released 2015-10-26 to 2016-01-18 to active teams; 53,258 rows together, computed from 133,151), testData.7z, working_site_metadata.csv and a file of column names. Boullé (FedCSIS 2016, Fig. 3, https://annals-csis.org/Volume_8/pliks/21.pdf) gives the schema: a root table (main_working_id, total_bumps_energy, total_tremors_energy, ..., latest_maximum_yield, latest_maximum_meter), an hourly table (hour, count_e2, count_e3, ..., avg_difference_in_gactivity, avg_difference_in_genergy) and the site table (main_working_name, region_name, bed_name, main_working_type, main_working_height, geological_assessment); the summary paper (Sec. III) names latest_seismic_assessment and latest_comprehensive_assessment among the 12. The page also says: "All competition data were made available in the Data files folder (including the labels for the test set".
- The task's table: one row per 24-hour window at a working site, labelled by the seismic energy of the next 8 hours. Training 133,151 windows (2010-05-05 to 2014-03-06), test 3,860 (2014-03-07 to 2015-06-24), stated. The training windows overlap: site 373 alone has 31,236 windows in a period of 1,402 days (33,648 hours, 4,206 eight-hour shifts), so consecutive windows lie about one hour apart (computed; the step is not stated). One window per 8-hour shift would leave about 16,644 training rows (133,151 / 8, an estimate). Inputs: 547 columns; 545 after the site id (the group) and the site name, 528 of them the hourly values of 22 measures; as distinct measures, 12 period values, 22 hourly series and 5 site fields. The second-placed team reduced each series to sums over 24 hours, the last 5 hours and the last hour, 133 features in all (deepsense.ai write-up).
- Access: Knowledge Pit login and enrolment in the challenge; 7z archives of CSV, sizes not stated; "The data set is free to use for non-commercial purposes", with a citation of the papers and a link to the platform (a note, EV-4).
- Changes the call: the published test labels settle the record's open risk: the organisers' split (SPLIT-19) is usable, with 3,860 labelled non-overlapping test windows from 21 sites, 8 of them absent from training (Table I). For the wide-table list: the 547 columns are an unrolled series of 22 measures, not 547 variables, and the screening's SEL-12 and SEL-11/TP-10 questions stay. Priority 4 stands.
- Not checked: the files (login); the names of the 22 hourly measures and of all 12 period values; the window step; whether the four additional training files repeat rows of the first.
