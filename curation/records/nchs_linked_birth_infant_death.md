---
unique_name: nchs_linked_birth_infant_death
name: NCHS linked birth / infant death data
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.cdc.gov/nchs/nvss/linked-birth.htm
- https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm
- '# user guide of the 2024 period / 2023 cohort files'
- https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/DVS/period-cohort-linked/24PE23CO_linkedUG.pdf
v2_path: datasets/_dev/tabarena-v0pt2/nchs_linked_birth_infant_death_1m/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-08):** `TBD -> Yes`, priority 2: the US birth certificates of one year (3,605,081 births in the 2023 cohort) linked to the 19,772 infant deaths among them, public-use files of NCHS for cohorts since 1983; death before age one from what the birth certificate records is a real risk task at a very large size, but the use case is ours, 0.55% are positive, and several items are recorded after the birth.
- Source: National Center for Health Statistics (NVSS), "Linked Birth and Infant Death Data" (page and the 2024 period / 2023 cohort user guide, read): "The linked birth/infant death data sets (linked files) for 2017 through 2024 are released in one format that can be used for both period data and birth cohort data". The numerator file holds the infant deaths linked to their birth certificates (record length 1,743), the denominator file all births (record length 1,346, the natality record). Counts (guide): the 2024 period file has 19,836 linked infant deaths (98.8% linked) and 3,638,436 births; the 2023 cohort 19,772 linked infant deaths (260 unlinked) and 3,605,081 births. Public-use files on Vital Statistics Online: combined period and cohort zips for 2017/2016 to 2024/2023 (422-450 MB each), period files 1995-2017, cohort files 1983-1991 and 1995-2015, "available for independent research and analyses" under NCHS's data use terms (no application).
- The task's table: one row per birth of a cohort year (3,605,081 for 2023: the denominator file joined to the deaths of the 2023 and 2024 numerator files, as the guide's "User Created Cohort" section does), target death before age one, x the birth-certificate items known at delivery (parents' age, race, education and marital status, prenatal care, pregnancy risk factors, plurality, gestational age, birth weight, delivery method and more; the count after dropping recodes and reporting flags is not stated). Access: open, about 0.4 GB a zip per year, fixed-width files with a user guide.
- Use case: a hospital's newborn team or a health department decides at the birth which infants get follow-up visits or a home-visiting programme. Ours: NCHS publishes the files for "more detailed analyses of infant mortality" (page). Fit direct for a model at delivery. Regime temporal by birth year.
- Siblings and duplicates: `nchs_natality_birth_weight` and `nvss_natality_pregnancy_outcomes` (both `TBD -> Yes`, priority 2) use the same birth records (the denominator file is the natality record) with other targets, a distinct task (PROV-7); the curator may want one task per birth register. No other infant-mortality record (grep: infant death, infant mortality, linked birth). External collections: none found.
- Better data: none searched (found by the data-scouting run of 2026-11-08).
- Papers and pages: the user guide; NVSR "Infant Mortality in the United States, 2024" (not read); many infant-death models on these files (not read).
- Metric: none found (the page and the user guide report rates only), so the fallback `roc_auc` (MET-1, MET-8). Inputs: none.
- Risks for /add-dataset: `ILIVE` ("Infant Living at Time of Report") gives early deaths away (LEAK-10, drop); the abnormal conditions of the newborn (NICU admission, assisted ventilation, surfactant, antibiotics, seizures), Apgar scores and the transfer flag are recorded after birth, so the prediction point (at delivery, or at discharge) decides whether they stay (USE-3, USE-4); the death record's fields (age at death, causes) are outcomes; imputation flags (`F_*`) and reporting flags are no inputs; the weight `recwt` is not for cohort files (guide); the 1.3% unlinked deaths count as survivors (small label noise); 0.55% positives on 3.6M rows need a cut that keeps every death (TP-8).
- Priority: gap 0 (medical, binary and temporal covered), use case 0 (ours), source + (NCHS files with a user guide per year), shape + (millions of births, many mixed items, many cohorts), risk - (post-birth items and the `ILIVE` leak).

Found by the data-scouting run of 2026-11-08 for the large-datasets review (wide tables outside biology and medicine, and tables with 2M+ rows).

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates, round 2 (wide tables outside biology and medicine, tables with 2M+ rows).

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: the co-twin's prior-birth counts blanked on later-born multiples, the cyanotic heart disease and the paternity acknowledgement dropped, the karyotype levels merged into Yes, LEAK-10; the 2017-2019 imputed birthweights blanked and the 'label-free' text corrected, LEAK-13; the 'plural delivery' interval code set missing, CLEAN-10; the unlinked deaths cited as LEAK-25; the release lag, the seed spread 0.004, the 2021 sampling fraction and the paper read stated; the use case narrowed to expected deaths at the birth); rebuttal round skipped (briefs converged); disputed: SEL-1 (race, every reviewer recommends dropping), LEAK-10/LEAK-6 (outcome-marked unknowns kept against mic and 2_month_survival), USE-3 (a second folder for the screen at registration), MET-8/MET-11 (log loss); for the curator: issues 1-4. Priority 2: gap 0, use case 0, source +, shape +, risk - (use case: ours, not the source's; risk: race and the outcome-marked unknowns are open).
