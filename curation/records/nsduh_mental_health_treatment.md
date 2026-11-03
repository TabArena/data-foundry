---
unique_name: nsduh_mental_health_treatment
name: 'National Survey on Drug Use and Health (NSDUH) public use files: adult mental health treatment'
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
source_links:
- https://www.samhsa.gov/data/data-we-collect/nsduh-national-survey-drug-use-and-health
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: SAMHSA's yearly national survey on drug use and mental health, proposed for the OSMI target "sought treatment"; a much larger probability sample, but whether a respondent received treatment is their own answer in the same interview, which no screening decision predicts (SEL-7 open).
- Source: Substance Abuse and Mental Health Services Administration (SAMHSA), National Survey on Drug Use and Health, conducted by RTI International; yearly public-use files, redesigned in 2015. SAMHSA's pages returned 403 here, so the sizes are the run's notes (about 56,000-69,000 respondents aged 12 and over a year, some 2,000-3,000 variables); a Kaggle copy of 2015-2019 (bgallamoza, 2.2 GB) says "All column names are identical to the Question Index found in the NSDUH documentation" and that the 2015 redesign created "broken trends". Target as proposed: received any mental health treatment in the past year (adults; a recoded variable of the codebook, not read), or a past-year major depressive episode from the survey's DSM-based module.
- Use case: an employer assistance programme, health plan or public health service targets outreach to adults likely to need or seek treatment; fit approximate at best: treatment receipt is a past behaviour the respondent reports in the same interview as the features, so nobody predicts it (SEL-7, as `cdc_diabetes_health_indicators`), and a depressive episode is scored from interview questions a screener would simply ask (USE-2 doubt); regime temporal by survey year if a target survives.
- Siblings and duplicates: `mental_health_tech` (`TBD -> 2nd Tier`, No Good Target (yet): OSMI 2014, "treatment: Have you sought treatment for a mental health condition?" per its Kaggle card); `nsduh_past_year_drug_use` (the same survey for drug-use targets: a distinct task under PROV-7, or one record with two targets, the curator decides); `mental_health_dataset` and `busara_mental_health_prediction_challenge` (other surveys). OSMI's later waves (https://www.kaggle.com/datasets/osmihelp/osmi-mental-health-in-tech-survey-2023, https://www.kaggle.com/datasets/osmihelp/osmh-2021-mental-health-in-tech-survey-results) are versions of the OSMI source (PROV-6), not NSDUH data: moved from the source links to here (PROV-12). External collections: none known (not searched: the run's web search budget was used up).
- Better data: found as better data for `mental_health_tech`; no further search this round.
- Papers and pages: the SAMHSA NSDUH page (403); the Kaggle copy's card.
- Metric: none found (no source defines a prediction task on it), so the fallback `roc_auc` (MET-8) if a target survives; inputs none (survey weights ship, but are no scoring input).
- Risks for /add-dataset: the target (SEL-7 for treatment receipt; for a depressive episode the module's items leave the features, LEAK-10); hundreds of items of the same interview to screen per target; the 2015 redesign; recodes and disclosure edits in the public file.
- Priority: gap 0, use case 0 (no decision fits the proposed target), source + (a federal survey with a codebook), shape + (tens of thousands of respondents a year), risk - (SEL-7).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `mental_health_tech`.
- as published: one row per respondent aged 12+, about 56,000-69,000 a year (adults about 40,000+), some 2,000-3,000 variables. Figures from memory: SAMHSA pages answered 403 to WebFetch, as they did to scout_25 ...; target: received any mental health treatment in the past year (adults; the codebook's recoded treatment variable), or a past-year major depressive episode from the ...; access: open.
- Why: The OSMI 2014 survey's usable target is 'treatment' (has the respondent sought treatment for a mental health condition) from age, gender, employment, coverage and family history. NSDUH asks the same question with features of the same kind (demographics, employment status, health insurance, psychological distress) in ...
- Adds: About 40 times the respondents per year, a probability sample instead of a self-selected online survey of tech workers, yearly waves for a temporal split, and a documented codebook. Trade-off: no tech-workplace policy items (benefits, wellness program, anonymity), so the population is all US adults, not tech workers. ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same NSDUH survey with two targets (`nsduh_past_year_drug_use`; PROV-7, weigh). The curator keeps one, or both as distinct tasks.
