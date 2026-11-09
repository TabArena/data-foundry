---
unique_name: msha_mine_injury_frequency
name: 'usMSHA1316: injuries per US mine-year from Mine Safety and Health Administration data, 2013-2016 (SOA exam data, CASdatasets)'
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: TBD -> Yes
priority: 3
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: Other
year: '2018'
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://dutangc.github.io/CASdatasets/reference/usMSHA1316.html
- https://doi.org/10.48550/arXiv.2112.14865
- https://variancejournal.org/article/116404-compositional-data-regression-in-insurance-with-exponential-family-pca
- https://www.msha.gov/data-and-reports/mine-data-retrieval-system
- https://www.soa.org/globalassets/assets/files/edu/2018/2018-12-exam-pa-data-file.zip
- https://www.soa.org/globalassets/assets/files/edu/2018/2018-12-exam-pa-project-statement.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 53,746 US mine-years (2013-2016) with the count of reported injuries and the employee hours as exposure, the data of the Society of Actuaries' December 2018 Predictive Analytics exam; a documented count task with a named actor, built from MSHA data with no mine id.
- Source: the Society of Actuaries, Exam PA December 2018 project statement ("Re: Mine Safety Ratings", read) and its data file (soa.org .../2018-12-exam-pa-data-file.zip, cited by Gan and Valdez): "The data is from the U.S. Mine Safety and Health Administration (MSHA) from 2013 to 2016. Each row represents the safety experience of one mine for one year. There are 20 variables—I have reworked them so most do not need extra interpretation"; its data dictionary names the "U.S. National Institute for Occupational Safety and Health Mining Program". Re-shipped in CASdatasets 1.2-1 as `usMSHA1316` (its Format block wrongly says 1,340 x 8; its example gives 53,746 x 20). Columns: YEAR, US_STATE, COMMODITY, PRIMARY, SEAM_HEIGHT, TYPE_OF_MINE, MINE_STATUS, AVG_EMP_TOTAL, EMP_HRS_TOTAL, ten PCT_HRS_* shares that sum to 1, NUM_INJURIES.
- Use case: "The union would like to give functioning mines in the United States a simple five-star safety rating to help their members when choosing where to work and negotiating hazard pay", with models "that will predict the rate of injuries per 2000 employee hours for a given mine" (project statement); an exam scenario, but a named actor and decision, and the same frequency model serves an insurer pricing workers' compensation. Fit direct for rating operating mines. Regime temporal: Gan and Valdez train on 2013-2015 and test on 2016 (Sec. 5), and a rating looks a year ahead; the same mine recurs across years without an id.
- Siblings and duplicates: the other CASdatasets records (`fremtpl2`, `bemtpl97`, `eudirectlapse`, `eumtpl`, `ausprivauto0405`, `swedish_motorcycle_insurance`) are other tables and tasks (PROV-7); `aaia16_coal_mine_seismic_hazard` is another mining task (seismic hazard). No duplicate (grep: msha, mine safety, CASdatasets). External collections: none known.
- Better data: from the curator's Zotero collection (item 302, the CASdatasets package index); no further search this round (the Assessment notes that MSHA's open mines, employment and accident files would allow a rebuild with mine ids and later years).
- Papers and pages: Gan and Valdez, "Compositional Data Regression in Insurance with Exponential Family PCA", arXiv 2112.14865 (2021; Variance 17(1), 2024), Sec. 3 (data) and Sec. 5 (negative binomial models and their validation), read; the CASdatasets page (read).
- Metric: the SOA memo prescribes a Poisson model of NUM_INJURIES with EMP_HRS_TOTAL/2000 as the offset, "Validation should be on NUM_INJURIES", and supplies the Poisson log-likelihood "in case it is helpful", but "Other methods for validating your models are fully acceptable"; Gan and Valdez score a Pearson chi-square over the numbers of mines with j injuries (Sec. 5.1), a portfolio statistic, not a per-row score. No fixed metric: the fallback `rmse` on the count, or a Poisson deviance with EMP_HRS_TOTAL as the exposure (ships) if the curator follows the memo (MET-1, MET-5).
- Risks for /add-dataset: an exam table the SOA "reworked", with "more data checking and cleaning to do—some records and/or fields should probably be eliminated" (the memo): look for planted errors and compare a sample with MSHA's raw files (PROV-3, PROV-13); EMP_HRS_TOTAL and AVG_EMP_TOTAL are the same year's exposure (correlation 0.9942, Sec. 3), known only at the year's end, so the task predicts a year's count from that year's exposure (USE-3); many zero counts; no mine id, so a mine's years cannot be grouped; MINE_STATUS terms differ between coal and other mines (the memo). Domain left empty: industry & manufacturing (mine safety) or insurance (the actuarial framing), the curator's call.
- Priority: gap 0 (industry & manufacturing, regression and temporal are not thin; insurance would be thin), use case + (the source names the union's rating decision), source + (the SOA project statement and data dictionary, a paper), shape + (53,746 mine-years, mixed types), risk - (an exam-reworked table with cleaning left to the candidate, no mine id).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 302: "Package index".
- as published: 53,746 mine-years x 20 columns: YEAR, US_STATE, COMMODITY, PRIMARY, SEAM_HEIGHT, TYPE_OF_MINE, MINE_STATUS, AVG_EMP_TOTAL, EMP_HRS_TOTAL, ten PCT_HRS_* shares of hours by work location, and ...; target: NUM_INJURIES: accidents reported per mine-year (count, with EMP_HRS_TOTAL as exposure); access: open.
- Why: Real regulator data with an actuarial count target and a published exam and paper. The original source (MSHA mines, employment and accident files) is maintained up to today, so a newer, larger build with mine ids is possible.
- Adds: A workplace-safety and occupational-insurance domain, with compositional features. Caveats: the same mine recurs across years without an id (grouped leak risk; rebuilding from MSHA's raw files would give ids and newer years), many zero counts, and the CASdatasets page's format block is wrong (it says 1,340 x 8).

**Assessment (AI, 2026-11-06):** under the rules adopted on 2026-11-06 (MET-14, MET-15, LEAK-41), /add-dataset ships the injuries per 2,000 employee hours (NUM_INJURIES / (EMP_HRS_TOTAL/2000), the memo's offset as the denominator) with EMP_HRS_TOTAL/2000 as the weight scoring column and the task's `sample_weight`, scored by `mean_poisson_deviance` with that `weight` input (the memo's Poisson model with the offset, "Validation should be on NUM_INJURIES"). Whether the hours are planned or realized (a mine closing after an accident cuts them) is the timing question of LEAK-41: as the denominator and weight they are never a feature, and AVG_EMP_TOTAL, which encodes them, needs the same check (probe 22). The curator has the call when the dataset is added.
