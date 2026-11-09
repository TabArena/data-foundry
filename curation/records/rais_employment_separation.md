---
unique_name: rais_employment_separation
name: RAIS (Relacao Anual de Informacoes Sociais) public de-identified microdata, employment links (RAIS Vinculos)
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/microdados-rais-e-caged
- https://basedosdados.org/dataset/3e7c4d58-96ba-448e-b053-d385a829ef00
- https://cran.r-project.org/web/packages/raisr/index.html
v2_path: datasets/_dev/tabarena-v0pt2/rais_employment_separation_1m/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: Brazil's annual census of formal employment (RAIS), public de-identified microdata with one row per employment link and year since 1985, from which a twelve-month separation target can be cut for the links active on 1 January; real administrative data at a scale no HR table has, but the cohort, the target and the features known on 1 January are ours to build.
- Source: Ministry of Labour and Employment (MTE), PDET programme, "Microdados RAIS e CAGED" (gov.br page, updated 2026-06-17): "microdados não identificados" of RAIS (establishment and worker files), ";"-delimited text files on ftp.mtps.gov.br/pdet/microdados/; RAIS is the report every employer must file (Decreto 76.900 of 1975, per Base dos Dados, which lists 1985-2025); raisr 0.1.0 (CRAN, 2026-09-29) reads "the public, non-identified microdata" with two header formats, up to RAIS 2022 and from 2023 (RAIS built from eSocial). As published (the fields as commonly documented, not re-read on the layout file in this screening): admission date, separation month and reason (quit, dismissal with or without cause, end of contract, retirement, death), active on 31/12, tenure, average and December pay, contracted wage and hours, occupation (CBO), sector (CNAE), establishment size, age, education, sex, race, municipality; tens of millions of links per year.
- Use case: an employer's HR team, at the start of the year, flags employees likely to quit within twelve months and decides on retention measures; the source names no prediction (a labour census for statistics), so the use case is ours. The employer decides dismissals itself, so the target is the quit, not every separation. Fit approximate (all employers pooled; no history per worker, since the public files carry no worker id). Regime temporal by base year (train on earlier years, test the next), SPLIT-6.
- Siblings and duplicates: `employee` (No, `Data Quality Issue`; Andrej: "Missing information on the target"), `happyforce_employee_churn` (TBD -> Yes, this run), `ibm_hr_analytics_employee_attrition_performance_employee_ibm_attrition` (No). No RAIS record before (grep rais, caged, pdet). External collections: none found.
- Better data: found as better data for `employee`; no further search this round.
- Papers and pages: the gov.br page, Base dos Dados (dataset 3e7c4d58) and raisr; papers that used RAIS for turnover prediction: not searched (the session's web-search budget ran out).
- Metric: none found (a census defines no task; the gov.br page, Base dos Dados and raisr checked), so the fallback `roc_auc` for a binary quit target (MET-8, MET-11); inputs none.
- Risks for /add-dataset: the cohort (links admitted before 1 January and active then) and the target (a quit within the year) to define from the separation month and reason (USE-5); fields recorded at year end or at separation (tenure, average and December pay, active on 31/12, perhaps the contracted wage after a raise) must not enter (LEAK-10); a sample from very large files; the 2022/2023 break in the series (eSocial); sex and race as inputs to an HR decision, an ethics note for the curator (SEL-1 is not triggered by the source).
- Priority: gap + (social science is thin), use case 0 (ours), source + (the ministry's census, with a decree and a file layout), shape + (millions of links per year over many years, mixed features), risk - (cohort and target to build; year-end fields leak).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `employee`.
- as published: one row per formal employment link and year, every formal employer in Brazil: tens of millions of links per year, about 60 columns; base years 1985 to the latest (Base dos Dados lists 1985-2025); ...; target: whether an employment link active on 1 January ends during the year, with the separation reason (quit, dismissal with or without cause, end of contract, ...; access: open.
- Why: The same target as the employee record (will this employee leave) with features of the same kind: education, age, sex, municipality, contracted pay, tenure from the admission date, plus occupation (CBO), sector (CNAE), establishment size, contracted hours and contract type. Real administrative records from a report ...
- Adds: A defined horizon and a separation reason, traceable official provenance (the Kaggle table names neither its company nor its horizon), millions of employees across all sectors and years instead of 4,653 employees of one unnamed company. Caveats: de-identified, so a worker cannot be followed across years or employers; ...

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: the five protected grounds, the armed forces and negative January pay out, fixed-term contracts of recent hires merged, the tenure rebuild fixed, the split, population and label notes written); disputed: LEAK-25 (the dormant links, settled by measurement as recorded outcomes), USE-8 (the pooled public servants and military); for the curator: issues 1-5. Priority 3: gap 0, use case 0, source +, shape +, risk 0 (gap: social science is not thin among the 151 accepted definitions; use case ours; risk: the leaks found are fixed; the open calls change the score's level and keep the order of models, except that leaving out the dormant links or keeping only the links paid in January swaps two adjacent learners, 0.0006-0.0012 apart, on 3 of 3 folds).
