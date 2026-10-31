---
unique_name: medicare_provider_leie_exclusion
name: CMS Medicare provider utilization and payment data (Physician & Other Practitioners by Provider; Part D Prescribers by Provider) labelled with the ...
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners/medicare-physician-other-practitioners-by-provider
- https://oig.hhs.gov/exclusions/exclusions_list.asp
- https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers/medicare-part-d-prescribers-by-provider
- https://doi.org/10.1186/s40537-018-0138-3
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: providers' yearly Medicare billing summaries from CMS, labelled by a later exclusion on the HHS OIG's LEIE list for fraud-related offences, the setup of a line of papers from Florida Atlantic University (Herland, Khoshgoftaar and Bauder 2018; Johnson and Khoshgoftaar 2023); real and traceable, but the table and its label are ours to build, and positives are under 0.1%.
- Source: no single release; public sources joined by NPI. CMS, "Medicare Physician & Other Practitioners - by Provider" and "Medicare Part D Prescribers - by Provider" (data.cms.gov; data years 2013 to 2024 in the CMS catalogue; one row per NPI and year with "use, payments, submitted charges and beneficiary demographic and health characteristics"); HHS OIG, List of Excluded Individuals and Entities (NPI, exclusion type such as 1128a1, exclusion date). The task as first set: Herland, Khoshgoftaar, Bauder, "Big Data fraud detection using multiple medicare data sources", J Big Data 5:29, 2018 (2012-2015 Part B, Part D and DMEPOS with LEIE labels). As rebuilt by Johnson and Khoshgoftaar, "Data-Centric AI for Healthcare Fraud Detection", SN Computer Science 2023 (PMC10173919): 2013-2019 data, "a subset of exclusion rules that are indicative of fraud" (following Bauder and Khoshgoftaar), a provider's claims up to the exclusion year plus the minimum exclusion period labelled positive, "rare fraudulent class sizes ranging from 0.0456 to 0.0880%", 31-38 features in the aggregated sets.
- Use case: CMS or OIG program-integrity staff, after a claim year, rank providers for audit or investigation ("Automated methods for detecting fraudulent healthcare providers have the potential to save billions of dollars", Johnson and Khoshgoftaar 2023, abstract); fit approximate: an exclusion follows a conviction or sanction, so undetected fraud is labelled negative (USE-5, USE-8). Regime grouped by provider at least, since a provider has a row per year: the same paper got "near-perfect AUC > 0.99" with providers in both train and test folds and proposed folds by NPI; a temporal split by claim year is the alternative (SPLIT-3, USE-10; decide at /add-dataset).
- Siblings and duplicates: `medical_provider_fraud_detection` (`TBD -> 2nd Tier`, Missing source information; a Kaggle file of 5,410 providers with no traceable source): the same task from another source, so its own record (PROV-4). No other record links the CMS provider files or the LEIE. External collections: none found.
- Better data: found as better data for `medical_provider_fraud_detection`; no further search this round.
- Papers and pages: Johnson and Khoshgoftaar 2023 (read in Europe PMC); Herland et al. 2018 (doi 10.1186/s40537-018-0138-3; full text not reachable, a Springer login redirect); "The effects of varying class distribution on learner behavior for medicare fraud detection with imbalanced big data", 2018 (PMC6120851, title only).
- Metric: none deliberate: the 2023 paper reports "AUC, AUPRC, TPR, and TNR" and G-mean as "complementary performance metrics", so the fallback `roc_auc` (MET-5, MET-8; MET-9: rarity alone is no reason for AUPRC); inputs none beyond the NPI as a group key (MET-2).
- Risks for /add-dataset: the table and the label are ours to build (PROV-11: CMS and the LEIE are the origin), with the exclusion rule codes and the labelling window to fix and document (USE-5); providers excluded after the LEIE download look negative in recent years (LEAK-22 to LEAK-26, SPLIT-9); 0.05-0.09% positives, so folds need enough of them (TP-5); names and NPIs are identifiers (keep the NPI only as the group key); the yearly files change columns over time (the 2023 paper matched columns across years).
- Priority: gap 0 (medical and binary are not thin; insurance would be thin if the curator files Medicare fraud there), use case 0 (named, but the fit is approximate), source + (documented CMS and OIG releases, papers that define the task), shape + (about a million providers a year, numeric and categorical, grouped and temporal), risk - (a table and label to build, a proxy label).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `medical_provider_fraud_detection`.
- as published: one row per provider (NPI) per year with services, beneficiaries, submitted charges and payments, specialty, place, and beneficiary age/risk/chronic-condition mix; on the order of a million Part B ...; target: provider excluded by OIG (LEIE exclusion, e.g. program-related fraud or patient abuse) after the claim year; access: open.
- Why: the same task as medical_provider_fraud_detection (flag providers as potential fraud from aggregated claims and beneficiary mix), from real, traceable public data with labels from a public enforcement list
- Adds: a named publisher and first publication against an untraceable Kaggle file (whose beneficiary table follows the schema of CMS's synthetic DE-SynPUF files, from memory, worth checking); about a million providers a year against 5,410; 2013-2024. Caveats: LEIE is a proxy label (exclusions, not all fraud; the file holds ...
