---
unique_name: nhanes_dxa_body_fat
name: NHANES whole-body dual-energy X-ray absorptiometry (DXX) with body measures (BMX)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/DXX_J.htm
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/DXX_G.htm
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BMX_L.htm
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: whole-body DXA percent fat with tape-and-scale body measures for about 4,000 people per NHANES cycle, the precedent the curation rules name for `body_density_prediction` (252 men, 1985); the target is the quantity body density stands in for, measured by a reference method.
- Source: CDC/NCHS NHANES DXA whole-body files: DXX_G (2011-2012) 5,692 records, 4,521 with total percent fat (DXDTOPF); DXX_J (2017-2018) 5,114 records, 3,658 with it; "Participants aged 8-59 years were eligible"; "Whole body DXA scans were administered from 1999-2006 and 2011-2018" (DXX_J). Joined by SEQN to the body measures BMX (weight, height, waist, arm and thigh circumference; hip from 2017-2018; skinfolds in 1999-2006, per the scout) and demographics. The 21,768 people of the precedent were not recounted; 2011-2018 alone should give about 16,000.
- Use case: a clinician, gym or fitness device estimates body fat from a tape and a scale instead of a DXA scan or underwater weighing (the curator on `body_density_prediction`: still "done by models in machines in gyms"); Woolcott and Bergman built Relative Fat Mass equations on NHANES 1999-2006 DXA (Sci Rep 2019, n = 10,390 aged 8-19, doi 10.1038/s41598-019-51701-z), "useful to estimate whole-body fat percentage and diagnose body fat-defined overweight or obesity"; fit direct; regime IID by person as on `body_density_prediction`, or temporal by cycle as the other NHANES records (DXA software versions changed across cycles, DXX_J): the curator decides.
- Siblings and duplicates: `body_density_prediction` (`Yes (Disagreement)`, shipped; Outdated, Not Representative, Too Small), `body_fat_prediction_dataset` (`No`, its duplicate); `nhanes_bmi_from_habits` (another target on the same exam, PROV-7). External collections: none known (not searched: the run's web search budget was used up).
- Better data: found as better data for `body_density_prediction`; no further search this round.
- Papers and pages: the DXX file pages; Woolcott and Bergman 2019 (abstract, read through Europe PMC).
- Metric: the RFM paper reports several accuracy measures (estimates within a range of the measured fat, obesity misclassification) without one ranked criterion (MET-5), so the fallback `rmse` in percent-fat points, as declared for `body_density_prediction` (MET-8); inputs none.
- Risks for /add-dataset: the 1999-2006 DXA was released with multiple imputations of missing scans (the scout's note; the 2011-2018 pages do not mention it): take one imputation or use 2011-2018 only; regional fat and lean of the same scan are outcomes, never features (LEAK-10); exclusions (pregnancy, over 450 lb or 6 ft 5 in, recent contrast) and "Whole body not scanned, other reason" (690 in 2017-2018) leave a selected sample; ages 8-59 only.
- Priority: gap 0 (medical, regression not thin), use case + (named by the curator and by the RFM papers), source + (NCHS documentation), shape + (about 16,000 people or more, mixed features), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `body_density_prediction`.
- as published: 21,768 people per the curator's precedent in selection.md (not recounted); one row per examined person; target DXDTOPF 'Total Percent Fat' plus regional fat/lean; features from BMX: weight, height, ...; target: whole-body percent fat by DXA, the quantity body density is a proxy for (Siri's formula), measured by a better reference method; access: open.
- Why: the precedent named in selection.md and SKILL.md step 3 for this exact record; same anthropometric features known at the prediction point
- Adds: about 86x the people of the 252 men from 1985, both sexes and ages 8-59+, a national sample; risks: 1999-2006 files are 5 imputations (use one, or the 2011-2018 cycles only), exclusions for pregnancy and >450 lb
