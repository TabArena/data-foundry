---
unique_name: pep725_fruit_tree_bloom_date
name: 'BloomBench: fruit-tree flowering dates (PEP725 and GMU cherry blossom data) with ERA5 daily weather'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
problem_type: Regression
source_links:
- https://github.com/WUR-AI/BloomBench
- https://openreview.net/forum?id=WSxIa8fPEX
- https://doi.org/10.5281/zenodo.15405663
- https://doi.org/10.1007/s00484-018-1512-8
- http://www.pep725.eu/
- https://arxiv.org/abs/2608.30392
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: observed flowering dates of fruit trees per station and year (PEP725 stations in Europe; cherry peak bloom in Japan, Switzerland and South Korea) with daily ERA5 weather as inputs, packaged as BloomBench; a real phenology task, but the inputs are raw daily series that a table has to summarise and the station-year panel sits near forecasting.
- Source: the observations come from PEP725, the Pan European Phenology database (Templ et al., "Pan European Phenological database (PEP725): a single point of access for European data", Int. J. Biometeorol. 62:1109-1113, 2018, doi 10.1007/s00484-018-1512-8; access by registration under its data policy), and from the cleaned data of George Mason University's cherry blossom prediction competition (Kyoto from Aono's series, Liestal from MeteoSwiss, Japan, Switzerland and South Korea; per-site copyright notices, Liestal for non-commercial use). BloomBench (Wageningen University, github.com/WUR-AI/BloomBench, created 2025-05-10) joins them with ERA5 daily mean temperature and daylight duration (Zenodo doi 10.5281/zenodo.15405663, 2025-05-14, 4 GB, Copernicus licence); the README says the paper is "TBA" and the OpenReview page (WSxIa8fPEX) could not be read. As published: one row per station, species and year with the flowering day of year (`bloom_doy`), the site's latitude, longitude and altitude; the weather comes as daily series per season. Counts of station-years not read.
- Use case: a fruit grower or an advisory service predicts the flowering date ahead of time to plan frost protection, pollination and spraying; fit approximate (the source pages name no actor). Regime temporal (later years) or grouped by station; BloomBench's split was not read.
- Siblings and duplicates: no phenology record (grep: phenolog, bloom, pep725, cherry blossom; `open_soil_spectral_library` only mentions a related word). External collections: BloomBench; the Zotero item (Nedungadi et al., "Foundation Models Meet Agriculture: Challenges Beyond Pretraining", arXiv 2608.30392) benchmarks seven agricultural datasets, phenology estimation among them.
- Better data: from the curator's Zotero collection, item 259; no new search this run.
- Papers and pages: Templ et al. 2018 (cited, not read); the BloomBench README and data READMEs; arXiv 2608.30392 (abstract).
- Metric: MAE in days, the one score BloomBench tabulates (`scripts/create_table.sh`: "Generate latex table rows containing MAE scores"), so `mae` if the paper confirms it as its criterion (MET-5); inputs none.
- Risks for /add-dataset: the inputs are daily weather series, in scope only where tabular models are competitive (SEL-12; BloomBench runs random forest, gradient boosting and AdaBoost against LSTM, GRU and CNN); a tabular version needs a cut-off date before bloom (the prediction point, USE-3) and summaries such as chill and forcing sums, features of our own making; one date per station and year, so check SEL-10 and SEL-11 against each station's naive profile (TP-10); 12 sub-datasets, so one species or a pooled task to choose; PEP725 access by registration (noted only, EV-4).
- Priority: gap 0 (environmental science, biology and regression are not thin), use case 0 (no actor named by the source), source + (the PEP725 data paper and a documented benchmark repository), shape + (many stations over decades), risk - (raw daily series to summarise, a forecasting-like panel).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 259: "Foundation Models Meet Agriculture: Challenges Beyond Pretraining".
- as published: station-years; 12 sub-datasets (GMU cherry Japan, Switzerland, South Korea; PEP725 apple, pear, peach, almond, hazel, cherry, apricot, blackthorn, plum); inputs are daily ERA5 mean temperature and ...; target: day of year of flowering (peak bloom or a BBCH flowering stage) at a station; access: registration.
- Why: real observed phenology dates from volunteer and met-service networks (an independent field observation, not computed from the features), many species and decades, location metadata; this Zotero item found TabPFN competitive on the maize variant
- Adds: a crop-phenology timing task, a gap among the records. Weak points: the inputs are raw daily weather series (like raw spectral bins, weighs out under SEL-12 and SEL-15), so a tabular version would use station, altitude and year plus chill and forcing sums up to a fixed cut-off date before bloom (prediction point); ...
