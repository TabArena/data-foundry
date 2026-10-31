---
unique_name: dhs_child_anemia
name: DHS child anemia (hemoglobin-tested children 6-59 months), Zambia 2018/2024 and pooled DHS surveys
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
source_links:
- https://dhsprogram.com/data/dataset/Zambia_Standard-DHS_2018.cfm
- https://doi.org/10.1101/2025.08.01.25332670
- https://api.dhsprogram.com/rest/dhs/surveys?countryIds=ZM&f=json
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-6): the same DHS children's-recode anaemia target (`hw57`, any anaemia in a haemoglobin-tested child 6-59 months, altitude-adjusted WHO thresholds) as `dhs_childhood_anemia`; Zambia 2018/2024 is another slice of the same DHS KR files, and the "pooled DHS surveys" framing is that record's pool, so this record adds no distinct task.
- Source: the DHS Program, Zambia DHS 2018 (fieldwork July 2018 to January 2019, released 2020-02-18) and Zambia DHS 2024 (fieldwork January to July 2024, released 2025-11-18), per the DHS API (api.dhsprogram.com/rest/dhs/surveys?countryIds=ZM); the ML paper Zulu et al., "Application of Machine Learning (ML) to Predict Under-Five Anemia using the 2018 Zambia Demographic and Health Survey (ZDHS)", medRxiv 2025-08-03 (doi 10.1101/2025.08.01.25332670): 7,743 children, 58.5% anaemic, Boruta selection, XGBoost accuracy 0.643 and AUC-ROC 0.673 on an 80/20 split with 5-fold CV; top predictors child's age, maternal anaemia, breastfeeding, region, stunting. The DHS API gives Zambia's child-anaemia indicator (CN_ANMC_C_ANY) as 58.1% (2018) and 51% (2024).
- Why a duplicate: both records end at the DHS Program's children's recode files with the same target (`hw57`) and the same kind of child, mother and household predictors (PROV-4); a single country's surveys are a cut of rows of the multi-survey pool (PROV-6: "another slice of the same cohort"). `dhs_childhood_anemia` (16 surveys, 68,856 children, a published leave-one-country-out protocol with AUC-ROC as its primary metric) is the record to keep; its dataset can take ZDHS 2018 and 2024 into the pool (the DHS API lists child anaemia for 177 surveys in 57 countries, 2000-2024), which the curator decides at add time. The curator may keep this name instead; one record should carry the task.
- Note for the kept record: the Zambia paper's second predictor is the mother's anaemia, measured in the same visit, a timing question for the prediction point (USE-3).
- Reject check (AI, 2026-10-31): stands. Both records use the DHS children's recode with the same target: 'The binary outcome was Anemia status, derived from the DHS hemoglobin indicator (hw57)' (Brima et al., Sec. 2.3, https://arxiv.org/html/2605.26589v1). This record's own second framing is 'pooled DHS surveys', which is the kept record's pool. Zambia is not among the paper's 16 surveys (Table 1), so ZDHS 2018/2024 are rows the pool can add, not a cut of it. PROV-6 counts added rows without a distinct task as a duplicate, and the Zambia paper's within-country split is a regime choice for the kept record. Fix the block's wording 'a cut of rows of the multi-survey pool': the Zambia rows are an addition.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 54: "Application of Machine Learning (ML) to Predict Under-Five Anemia using the 2018 Zambia ...".
- as published: children: 7,743 with a hemoglobin result in ZDHS 2018 (kids recode ZMKR71); child anemia is measured in 177 DHS surveys in 57 countries, 2000-2024; target: any anemia in a child aged 6-59 months (altitude-adjusted Hb < 11 g/dL; hw57 mild/moderate/severe vs not); access: registration.
- Why: Real survey measurements with a lab-measured target and a public-health decision attached; the newer 2024 wave and the multi-country pool make it much larger than the paper's single survey.
- Adds: No DHS anemia record. Version: ZDHS 2024 is a newer wave of the same source (PROV-6). Risks: maternal anemia, stunting and wasting are survey measurements (check which ones a screening visit has); DHS terms require registration and forbid redistribution (a note, not a reject).

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: correction to the block above: Zambia is not one of the pooled paper's 16 surveys, so its rows are an addition, not a cut of the pool.
