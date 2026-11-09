---
unique_name: uniform_soybean_tests_yield
name: Uniform Soybean Tests yield with genotype and daily weather (Shook et al. 2021)
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2021'
domain: biology & life sciences
problem_type: Regression
source_links:
- https://github.com/tryambakganguly/Yield-Prediction-Temporal-Attention
- https://doi.org/10.1371/journal.pone.0252402
- https://drive.google.com/drive/folders/1BLK56s_9z_O1DKJVGq10eKa-U5AykNY0
- https://doi.org/10.4231/r7hd7spk
- https://eval.ai/web/challenges/challenge-page/1251/overview
- https://github.com/itsMustafamr/Yield
v2_path: datasets/_dev/tabarena-v0pt2/uniform_soybean_tests_yield/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 103,365 variety-by-location-by-year yield records of the USDA-coordinated Uniform Soybean Tests (2003-2015) with maturity group, genotype, location and the season's daily weather, the data of the MLCAS2021 yield challenge (RMSE); real and large, but the season's weather is known only at harvest and every record of one environment shares it.
- Source: Shook, Gangopadhyay, Wu, Ganapathysubramanian, Sarkar, Singh, "Crop yield prediction integrating genotype and weather variables using deep learning", PLOS ONE 16(6):e0252402 (2021-06-17, https://doi.org/10.1371/journal.pone.0252402): the UST reports of 2003-2015 (public yield trials since 1941, published as PDFs and converted to spreadsheets), 103,365 performance records, 5,839 genotypes, 150 locations in 28 US states and Canadian provinces; per record maturity group, genotype (20 K-means clusters of a 5,839 x 5,839 pedigree relatedness matrix), location, and 214 days (1 April to 31 October) of 7 weather variables from a 30 km grid; target seed yield in bu/acre. "Relevant codes and the dataset are available in the GitHub link" (https://github.com/tryambakganguly/Yield-Prediction-Temporal-Attention), which points to a Google Drive folder (no files shown without sign-in on 2026-10-31). The MLCAS2021 Crop Yield Prediction Challenge (EvalAI 1251, 2021-09-03 to 2021-10-26, read through the EvalAI API) released it as numpy arrays: 93,028 training and 10,337 test records; inputs_weather (214 x 7 per record), inputs_others (MG, Genotype ID, State, Year, Location), yield, clusterID_genotype; "Please do not use this dataset for commercial use without permission" (a term, EV-4). The northern-region UST reports are on PURR (Nowling et al. 2018, https://doi.org/10.4231/R7HD7SPK, CC0, 1989-2021, print-formatted tables).
- Use case: a soybean breeder judges how lines perform across environments to decide which to advance and where (the challenge: "improve agricultural breeding", "a variety's plasticity"); fit approximate: the season's weather is an input known only at harvest, so the model explains genotype-by-environment yield after the season rather than forecasting it at planting; regime grouped or temporal: the paper and the challenge split at random (80/10/10), Rafi et al. 2026 split 86,101 records chronologically; held-out years or locations mirror a breeder's new environments (SPLIT-3).
- Siblings and duplicates: `genomic_prediction_soy_yield` (`TBD -> Yes`, 3; soybean yield from SNP markers, TabBench-Bio): another source and other inputs, no duplicate (PROV-7); `soybean` (UCI disease classes): unrelated. External collections: MLCAS2021 (EvalAI); Rafi et al. 2026 ("US Soybean Yield", 86,101 samples, a processed cut; https://github.com/itsMustafamr/Yield, about 86k sequences with 5 plant columns).
- Better data: from the curator's Zotero collection (item 166, Rafi et al. 2026); no further search this round.
- Papers and pages: Shook et al. 2021 (LSTM with temporal attention, MAE 5.441 bu/acre, R2 0.796 on a random 10% test); Rafi, Ayanlade, Ganapathysubramanian, Sarkar, Krishnamurthy, Hegde, Balu, "Benchmarking Tabular Foundation Models for Agricultural Yield Prediction" (Agri AI workshop at AAAI 2026: weather summarised per season, chronological 80/10/10 split, best RMSE 5.84 bu/acre).
- Metric: "We will use Root Mean Square Error (RMSE) as the evaluation metric" (EvalAI 1251, evaluation details), a leaderboard metric, so `rmse` in bu/acre (MET-4); inputs none.
- Risks for /add-dataset: the weather is a 214 x 7 daily series per record, shared by every line of a location-year, so it needs a season summary (weekly means, as the paper) and acts as an environment code (check against environment means, TP-10 style); a random split puts each environment in train and test; Genotype ID has 5,839 levels; plot traits measured at harvest (protein, oil, lodging, seed size) appear only in rebuilds from the UST reports and go if any arrive (LEAK); only the 93,028 training records may have released yields (to check); access through Google Drive or EvalAI to confirm.
- Priority: gap 0 (biology, regression and grouped are covered), use case 0 (approximate: the weather is known after the season), source + (PLOS ONE paper, a challenge, USDA trial reports), shape + (103,365 records, categorical and numeric inputs over years and locations), no known risk counted (the weather timing is scored under the use case).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 166: "Benchmarking Tabular Foundation Models for Agricultural Yield Prediction".
- as published: 103,365 performance records (variety x location x year), 2003-2015, 5,839 genotypes, about 150 locations; per record maturity group, genotype cluster, location and 214 days x 7 daily weather ...; target: Seed yield (bu/acre), regression; access: open.
- Why: Large, real multi-environment trial data with a documented source; the 86,101-record set in the item matches it.
- Adds: Large agricultural regression with grouped structure. Caveats: the season's weather is known only at harvest (an ex-post G x E model); plot traits such as protein, oil, lodging and seed size are measured at harvest (leaks for a yield task); data on Google Drive with no licence stated for the merged files (PURR ...

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).

**Assessment (AI, 2026-11-09):** added (/add-dataset, builder) as `datasets/_dev/tabarena-v0pt2/uniform_soybean_tests_yield/`; no size check of 2026-11-08 was in this record. Access: the challenge's zip link (Drive 1DoyextA0q4mxumMAhBvqZbfZriIM9A-Y) answers 404 and the paper's Drive folder lists no files (2026-11-09); the definition reads a copy of the challenge zip that a participant of the University of Arizona's 2021 course INFO 529 put on CyVerse on 2021-10-23 (files dated 2021-08-30, shapes as on the challenge page: 93,028 + 10,337 records, 214 x 7 weather, 5,839 clusters), named in the download instructions. Only the 93,028 training records have yields (the challenge never published the test yields); 214 exact copies dropped, 92,814 ship with 1,504 features (daily weather as released). Split: held-out seasons, 7 yearly windows 2009-2015 (the 2009 window added after the review panel), in place of the challenge's random split, under which every test location-year and line was in training. Measured: untuned models barely beat the training mean (LightGBM RMSE 16.59 against 16.68), each location's earlier mean reaches 13.71 and adding the weekly weather to a location-mean model makes it worse (13.92 against 13.15, on 5 of 6 windows): beyond each location's mean and the yield trend the weather adds nothing measurable for the models tried. Sibling `genomic_prediction_soy_yield` (SoyNAM project trials 2011-2013, SNP inputs, line values) shares no records or trials with the UST reports; line identity cannot be checked as the UST line ids are anonymized (PROV-7: distinct tasks).

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: the use case reworded to the paper's aim with the breeder or UST coordinator as actor, the copy's match with the authors' GitHub files written down, the 2009 window added, AvgSur_d213's impossible cells set to missing, a LEAK-9 protocol line, the notes' numbers and wording corrected); disputed: the metric (MET-1, MET-2, MET-4: RMSE against mean_group_pearsonr within location-year x maturity group, Kendall tau 0.38 between the two model orders, decided with genomic_prediction_soy_yield); for the curator: issue 1. Priority 3: gap 0, use case 0 (written from the paper's aim, fit approximate), source + (PLOS ONE paper and its challenge; the copy matches the authors' files), shape +, risk 0 (no leak in the data; the later-season exploit is covered by the protocol line).
