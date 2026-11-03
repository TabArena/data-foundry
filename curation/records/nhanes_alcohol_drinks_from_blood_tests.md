---
unique_name: nhanes_alcohol_drinks_from_blood_tests
name: NHANES alcohol use (ALQ) with the standard biochemistry profile (BIOPRO) and complete blood count (CBC)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://wwwn.cdc.gov/nchs/nhanes/
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/ALQ_J.htm
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/BIOPRO_J.htm
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/CBC_J.htm
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: NHANES measures the five BUPA blood tests (MCV, ALP, ALT, AST, GGT) and asks about drinking for thousands of adults per cycle, a measured, national version of `blood_tests_drink_prediction`'s task; the sibling's open use-case doubt (asking is easier than testing, and the target is self-reported) carries over unchanged.
- Source: CDC NCHS, NHANES (wwwn.cdc.gov/nchs/nhanes); 2017-2018 files: ALQ_J (adults 18 and over, 5,533 records, asked in the examination centre; ALQ121 "During the past 12 months, about how often did {you/SP} drink any type of alcoholic beverage?" in 11 frequency codes; ALQ130, the average drinks on drinking days, 1 to 14 with 15 for "15 drinks or more", 3,489 answers), BIOPRO_J (6,401 records, ages 12 and over, Roche Cobas 6000: ALT LBXSATSI, AST LBXSASSI, ALP LBXSAPSI, GGT LBXSGTSI), CBC_J (MCV; page not opened). Joined on SEQN; earlier cycles ask the frequency in other items (to check per cycle).
- Use case: a GP spots hazardous drinking from routine blood work when a patient under-reports; but the label is the patient's own report, so a model learns what people admit; the curators' discussion on the sibling ("If a doctor has the time to collect blood samples, asking for drinking behavior is simple") applies as it stands; fit approximate; regime IID by participant (temporal by cycle possible).
- Siblings and duplicates: `blood_tests_drink_prediction` (`Yes (Disagreement)`, BeyondArena; 345 men of the BUPA study, a regression on drinks, `Not Representative`, `Selection Bias`); `nhanes_liver_elastography_fibrosis` (unscreened; BIOPRO with another target); the other NHANES records of this run hold other targets (PROV-7). External collections: none found.
- Better data: found as better data for `blood_tests_drink_prediction`; no further search this round.
- Papers and pages: the NHANES codebooks named above.
- Metric: none found (NHANES documents a survey), so the fallback; the sibling declares `rmsle` on drinks per day with a log1p target, which this would follow (MET-3, MET-8); inputs none.
- Risks for /add-dataset: the target is self-reported at the same visit as the blood draw (an SEL-7 doubt: the participant knows it; not a past diagnosis, so not decided here); drinks per day is derived from frequency times quantity, with the codes harmonised across cycles; the non-drinkers (ALQ121 = 0) are a mass at zero; public files hold adults only; adding age, sex, BMI or the other analytes changes the task from the sibling's five tests, the curator's call.
- Priority: gap 0, use case 0 (the sibling's open doubt), source + (CDC codebooks), shape + (thousands of adults per cycle, many cycles), risk - (a self-reported target derived from questions that changed).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `blood_tests_drink_prediction`.
- as published: one row per examined adult, joined on SEQN; several thousand adults per cycle with the alcohol interview and both lab panels (not counted); the five BUPA blood tests are all there: LBXMCVSI (MCV), ...; target: average alcoholic drinks per day (ALQ130 'Avg # alcohol drinks/day - past 12 mos' on drinking days, times the drinking frequency ALQ121/ALQ120Q), the quantity ...; access: open.
- Why: same target and the same five features, measured in a national probability sample instead of 345 men selected in one study
- Adds: tens of thousands of adults of both sexes against 345 men from the 1980s, a documented lab protocol and population, age/sex/BMI available, temporal split by cycle; does not answer the record's use-case doubt (asking is easier than testing), and the target is self-reported as in BUPA
