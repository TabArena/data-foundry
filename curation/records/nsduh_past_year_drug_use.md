---
unique_name: nsduh_past_year_drug_use
name: National Survey on Drug Use and Health (NSDUH) public use files
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.samhsa.gov/data/data-we-collect/nsduh-national-survey-drug-use-and-health
- https://www.datafiles.samhsa.gov/dataset/national-survey-drug-use-and-health-2015-nsduh-2015-ds0001
- https://www.kaggle.com/datasets/bgallamoza/national-survey-of-drug-use-and-health-20152019
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and previews of the published tables, NOT from a built dataset. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: SAMHSA's federal drug-use survey, a probability sample of tens of thousands of respondents a year with a codebook, but the target is the respondent's own report of past-year use in the same interview as the features, and no source defines a prediction task on it (the doubt already open on `drug_consumption`; SEL-3, SEL-7).
- Source: Substance Abuse and Mental Health Services Administration (SAMHSA), National Survey on Drug Use and Health, conducted by RTI International; one public use file per year on SAMHDA, 2015 onward one series after the 2015 redesign. As published: one row per respondent aged 12 or older, coded items with a codebook; the scout's figures (about 56,000 respondents and 2,000-3,000 variables per file) could not be verified, since the SAMHSA and SAMHDA pages answer 403 to automated fetches. A Kaggle copy (bgallamoza, 2021, DbCL) stacks 2015-2019 into one 2.2 GB CSV under the codebook's variable names and names SAMHDA as its source.
- Use case: none named by the source. SAMHSA presents the survey as the "leading source of statistical information on the use of illicit drugs, alcohol, and tobacco and mental health issues in the United States" (quoted on the Kaggle card), i.e. weighted prevalence estimates. The scout's reading (prevention programmes targeting people at risk) is written by the curation and does not count (USE-1); fit approximate at best. Regime temporal by survey year if kept.
- Siblings and duplicates: `drug_consumption` (Fehrman et al. 2015, UCI; `TBD -> 2nd Tier`, `No Good Target / Scientific Discovery`, the SEL-7 doubt on self-reported use) has the same per-drug targets from an online convenience sample; `nsduh_mental_health_treatment` is the same survey with another target (PROV-7, a distinct task; the curator may want one NSDUH task, not two). External collections: none found.
- Better data: found as better data for `drug_consumption`; no further search this round.
- Papers and pages: the SAMHSA NSDUH page and the SAMHDA file pages (403 here); the Kaggle copy's card. Papers that model drug use on NSDUH were not searched: the session's web search budget ran out.
- Metric: none found (SAMHSA reports weighted estimates; the Kaggle copy defines no task), so the fallback `roc_auc` for a binary past-year-use target (MET-1, MET-8).
- Risks for /add-dataset: settle the target first: which drug, and past-year use or initiation among those who had never used (SEL-3, SEL-7, USE-5); the other substance, dependence and treatment items of the same interview, and the recency and age-at-first-use items of the drug itself, are near-proxies of the target (LEAK-10); analysis weights, strata and PSU are design columns, never features; coded missing and skip values need decoding (CLEAN-12).
- Priority: gap 0 (medical & healthcare and binary are not thin), use case 0 (written by the curation), source + (a federal survey with a codebook), shape + (tens of thousands of respondents a year, many coded items, yearly waves), risk - (a self-reported target without a task definer, SEL-3 and SEL-7 open).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `drug_consumption`.
- as published: one row per respondent aged 12+, about 56,000-59,000 respondents per annual public use file (e.g. about 56,100 in 2019), some 2,000-3,000 variables; figures from memory, since SAMHSA and ICPSR pages ...; target: past-year (or lifetime) use of a given drug, per drug (cannabis, cocaine, heroin, hallucinogens, methamphetamine, misuse of opioids, ...), the same per-drug ...; access: open.
- Why: same targets (self-reported use of each drug) and features of the same kind (demographics, education, psychological distress and depression scales); the federal standard survey on the question the Fehrman survey asks, from a probability sample instead of an online convenience sample
- Adds: about 30x the respondents per year, recent waves (to 2023), a probability sample, a documented codebook, years for a temporal split. Gaps: no Big Five personality scores (the core features of drug_consumption); many items on other substances are asked in the same interview and must be excluded per target (SEL-7, ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same NSDUH survey with two targets (`nsduh_mental_health_treatment`; PROV-7, weigh). The curator keeps one, or both as distinct tasks.
