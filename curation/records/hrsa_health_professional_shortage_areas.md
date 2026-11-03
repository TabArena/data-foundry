---
unique_name: hrsa_health_professional_shortage_areas
name: Health Professional Shortage Areas
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Regression
source_links:
- https://data.hrsa.gov/topics/health-workforce/shortage-areas
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/health-professional-shortage-areas
- https://arxiv.org/abs/2605.12292
- https://data.hrsa.gov/DataDownload/DD_Files/BCD_HPSA_FCT_DET_PC.csv
- https://data.hrsa.gov/DataDownload/DD_Files/BCD_HPSA_FCT_DET_DH.csv
- https://data.hrsa.gov/DataDownload/DD_Files/BCD_HPSA_FCT_DET_MH.csv
- https://data.hrsa.gov/DataDownload/DD_Files/HPSA_DATAMART_METADATA.XLSX
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: HRSA's register of designated health professional shortage areas, where STRABLE predicts the HPSA score, a priority score HRSA computes by published criteria; part of its inputs ship as columns (population-to-provider ratio, poverty share, shortage), the rest do not, and no decision predicts the score.
- Source: HRSA Bureau of Health Workforce, HPSA downloads (`BCD_HPSA_FCT_DET_PC`, `_DH`, `_MH` on https://data.hrsa.gov/data/download; dictionary `HPSA_DATAMART_METADATA.XLSX`): "HPSA Score ... developed by the National Health Service Corps (NHSC) in determining priorities for assignment of clinicians. The scores range from 0 to 26 where the higher the score, the greater the priority." As used by STRABLE (HF parquet, previewed): 9,691 rows x 57 columns (dental 6,575, primary care 1,662, mental health 1,454; geographic, population and facility designations), target `HPSA Score` in 27 integer values; `HPSA Formal Ratio`, `% of Population Below 100% Poverty`, `HPSA Shortage`, `HPSA FTE` and `HPSA Degree of Shortage` filled for about half the rows (the geographic and population designations).
- Use case: none in the source; HRSA scores each designation from the data a state primary care office submits, and the NHSC uses the score. Fit none to approximate; regime IID (current designations).
- Siblings and duplicates: no duplicate (grep for HPSA, shortage); `hrsa_clinician_dashboard` (its `Score` is this score at an alumnus's location). The record also carries STRABLE's "Medically Underserved Areas" table as its fourth link (`MUA_DET`, 3,882 rows x 51 columns, target `IMU Score`): a different HRSA file and target (PROV-7), so it needs its own record if kept; HRSA's MUA dictionary builds the IMU from four component values and their weighted IMU scores (providers per 1,000 population, infant mortality rate, share below the poverty level, share aged 65 and over), which `MUA_DET` ships and STRABLE dropped. External collections: STRABLE (Table C.4 rows 53 and 73).
- Better data: a candidate of the benchmark STRABLE; no further search for this run's finds.
- Papers and pages: the HRSA dictionaries above; the scoring criteria page (bhw.hrsa.gov) refused automated requests (403), so the score's components (ratio, poverty, infant health or fluoridation, travel time) are from general knowledge, to verify; 42 CFR Part 5 holds the designation criteria and degree-of-shortage groups; STRABLE, Blayer et al., arXiv 2605.12292 (v2, 2026-10-19).
- Metric: none found (STRABLE's R², App. D.1, is benchmark-wide, MET-5), so the fallback `rmse`; inputs none.
- Risks for /add-dataset: a score computed by a published rule with part of its inputs as columns (SEL-5: drop them and see whether a task remains, else `Trivial`, TP-4); facility designations (health centres, rural health clinics, IHS and tribal sites, prisons) are scored from data not in the file; the MUA table belongs in a separate record.
- Priority: gap 0, use case 0, source + (HRSA dictionaries), shape + (9,691 designations, 56 mixed columns), risk - (computed target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 9,691 rows x 57 columns incl. target (STRABLE parquet); target: HPSA Score.
- Why: Predict the HPSA score of a designated health professional shortage area | Predict the Index of Medical Underservice (IMU) score of a designated area
- Notes: HRSA HPSA download. The HPSA score is computed by HRSA from component scores; check whether the components are among the 57 columns. | Raw file MUA_DET.xlsx (HRSA). IMU is a formula of four component scores; check whether they are among the 51 columns.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: STRABLE's separate underserved-areas table is inside this record and needs its own.

**Assessment (AI, 2026-11-01):** STRABLE's medically underserved areas table moved to its own record, `hrsa_medically_underserved_areas`, on 2026-11-01; this record now holds the one table its name says (the screening block above still mentions the other).
