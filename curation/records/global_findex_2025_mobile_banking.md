---
unique_name: global_findex_2025_mobile_banking
name: 'The Global Findex Database 2025: Connectivity and Financial Inclusion in the Digital Economy (world microdata)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2025'
domain: finance
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://microdata.worldbank.org/catalog/7860
- https://microdata.worldbank.org/catalog/7860/data-dictionary
- https://microdata.worldbank.org/catalog/7860/get-microdata
- https://www.worldbank.org/en/publication/globalfindex
- https://doi.org/10.48529/bk9n-8r43
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the same World Bank Findex 2025 file as `global_findex_2025`, with mobile or internet use of an account as target; a traceable, documented source for the iX challenge's kind of rows, but a survey for measurement whose target is the respondent's own answer, the target variable is still to pick, and it is a second framing of one file.
- Source: as `global_findex_2025`: World Bank Development Research Group, Global Findex 2025, Gallup fieldwork 2024-05-01 to 2024-12-31, microdata version 02 of 2025-09-24 (https://doi.org/10.48529/bk9n-8r43, added to source_links; catalog 7860). As published: about 145,000 adults in 141 economies with survey weights; the run read the main file findex_microdata_2025_labelled_update112425 as 144,090 cases x 199 variables (not checked here); the waves of 2011, 2014, 2017 and 2021 are in the same library. Target: whether the respondent used a mobile phone or the internet to access an account or make a digital payment; the exact variable is to pick in the data dictionary (https://microdata.worldbank.org/catalog/7860/data-dictionary).
- Use case: none named by the source (a resource "for policy makers in the fields of digital connectivity and financial inclusion"); the record's reading is a bank or mobile-money provider choosing segments for mobile or internet banking products; fit approximate (SEL-7, as for the sibling); regime IID (one cross-section; a grouping by economy is possible).
- Siblings and duplicates: `global_findex_2025` (same file, account ownership; PROV-6 to weigh: a swapped target of the same respondents, as `arsenic_male_lung` against `arsenic_male_bladder`; at most one framing should enter, with the other named in its comments); `ix_mobile_banking_prediction_challenge` (`TBD -> 2nd Tier`, priority 1, the same target from an unnamed survey; its sibling UmojaHack 2021 #3 used Findex 2017); `dont_overfit_by_uofk_fmsi` (`No`, SEL-7). External collections: none known.
- Better data: no new search; found as better data for `ix_mobile_banking_prediction_challenge`.
- Papers and pages: the Microdata Library catalog page (read) and data dictionary (not read); the Global Findex 2025 report page (not read).
- Metric: none found (catalog page); fallback `roc_auc` (MET-1, MET-8). Inputs: the survey weight ships.
- Risks for /add-dataset: the target variable is not picked yet (an unclear target); answers on account use, payments and phone use for finance overlap with the target (LEAK); SEL-3 and SEL-7 as for the sibling; adults without an account cannot use one, so the target nests account ownership (decide whether to restrict the rows to account holders).
- Priority: gap 0 (finance, binary and IID are not thin), use case 0 (none named), source + (World Bank, codebook, weights), shape + (about 145,000 adults, mixed types), risk - (an unclear target variable, the SEL-7 doubt, a second framing of one file).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `ix_mobile_banking_prediction_challenge`.
- as published: adults (respondents), about 145,000 in 141 economies; main file findex_microdata_2025_labelled_update112425 144,090 cases x 199 variables; one wave (2024); earlier waves 2011, 2014, 2017, 2021 in ...; target: whether the respondent used a mobile phone or the internet to access an account or make a digital payment (Findex account-use questions; exact variable to ...; access: registration.
- Why: the same target as the iX challenge (uses mobile or internet banking) from a named, documented multi-country survey with weights and a codebook; the iX page names no survey (the sibling UmojaHack 2021 #3 challenge was Findex 2017), so this is the traceable, newer source of the same kind of rows
- Adds: traceable first publication (PROV-1) instead of an unnamed survey, fieldwork 2024 instead of an unknown year, survey weights, a questionnaire and codebook to check which answers would give the target away; similar size (144k vs ~145k). Caveat: the SEL-7 doubt of the iX record (a respondent's own answer as target, cf. ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: two targets of one survey file (`global_findex_2025`; PROV-7, weigh). The curator keeps one, or both as distinct tasks.
