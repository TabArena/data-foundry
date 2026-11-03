---
unique_name: nhanes_bmi_from_habits
name: NHANES measured body mass index with diet behaviour, physical activity, alcohol and smoking questionnaires
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://wwwn.cdc.gov/nchs/nhanes/
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/BMX_J.htm
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/DBQ_J.htm
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/PAQ_J.htm
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: NHANES measures height and weight (BMXBMI) and asks diet, activity, alcohol and smoking questions of thousands of adults per cycle, a national and measured version of `obesity_estimation`'s habits-to-BMI task (488 real web answers there); the use case is as thin as the sibling's.
- Source: CDC NCHS, NHANES; 2017-2018: BMX_J (8,704 records, ages 2 and over; BMXBMI from measured weight and standing height, 8,005 valid), DBQ_J (9,254 records; DBQ700 how healthy the diet is, ages 16 and over, asked at home; DBD895 meals prepared away from home and DBD900 meals from fast-food or pizza places in the past 7 days; DBD905 and DBD910 ready-to-eat and frozen foods in the past 30 days), PAQ_J (physical activity; page not opened), ALQ_J and the smoking file. Joined on SEQN; cycles can be stacked.
- Use case: a public-health or wellness programme estimates obesity from a habits questionnaire where nobody is measured; the source names none and a scale is cheap, the same doubt as on `obesity_estimation` (shipped as `Yes`); fit approximate; regime IID by participant (temporal by cycle possible).
- Siblings and duplicates: `obesity_estimation` (`Yes`, BeyondArena; 488 real rows once the SMOTE rows and repeats were dropped, BMI regression with height and weight removed); `nhanes_dxa_body_fat` (unscreened; body fat from body measures, another target); `body_density_prediction`. No duplicate (other targets, PROV-7). External collections: none found.
- Better data: found as better data for `obesity_estimation`; no further search this round.
- Papers and pages: the NHANES codebooks; Palechor and De la Hoz 2019, Data in Brief 25:104344, for the sibling's questionnaire.
- Metric: none found, so the fallback `rmse` on BMI, as on the sibling (MET-1, MET-8); inputs none.
- Risks for /add-dataset: keep every weight item out (BMI is weight over height squared, so drop measured weight and height, SEL-5; also the weight-history file's self-reported weight and any "told overweight" item; LEAK-10); reverse causation (heavier people report dieting or a "healthy" diet), so the signal may be weak (TP-2); questions change across cycles (the activity questionnaire was redesigned in 2007-2008, to check); survey weights; adults only, since children's BMI is read against age percentiles.
- Priority: gap 0, use case 0, source + (CDC codebooks), shape + (thousands of adults per cycle, mixed types), risk - (weight items to keep out, a thin use case).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `obesity_estimation`.
- as published: one row per adult, joined on SEQN; about 5,000 examined adults per cycle (not counted); target BMXBMI (measured); habits: DBQ700 how healthy is the diet, meals not home prepared, fast-food meals, ...; target: body mass index, measured by examiners (the record's target, self-reported by web volunteers there); access: open.
- Why: same target and the same kinds of habit features (meal frequency, eating out, vegetables/diet quality, activity, transport, screen/sedentary time, alcohol, smoking) as Palechor and De la Hoz's questionnaire
- Adds: a national probability sample of tens of thousands against 488 real web-volunteer rows, a measured target instead of self-report, no SMOTE rows; the habit items differ in wording from the source's
