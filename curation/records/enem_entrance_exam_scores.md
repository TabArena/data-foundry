---
unique_name: enem_entrance_exam_scores
name: Microdados do ENEM (Exame Nacional do Ensino Medio), INEP
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: education
problem_type: Regression
source_links:
- https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: INEP's ENEM microdata, millions of registrants per edition with their socioeconomic questionnaire and scores, a documented government source for the entrance-exam task; education is thin, but the source names no use and the race column needs the curator's call.
- Source: INEP (Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira), Microdados do ENEM, one zip per edition from 1998 to 2025 (https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem). The page: the microdata hold "as provas, os gabaritos, as informações sobre os itens, as notas e o questionário respondido pelos inscritos no Enem"; the editions 2019 to 2024 add a file of the essay graders' detailed scores. Rows and columns per edition were not read here (no zip was opened; each edition ships a Leia-me and a dictionary).
- Use case: a state education department or a school, at registration, targets exam preparation at candidates likely to score low; fit approximate: INEP publishes the data for research, not for a decision, and the score itself feeds university admission (SISU), which a prediction does not replace; regime temporal across editions (a later cohort), or IID within one edition.
- Siblings and duplicates: `student_performance_on_an_entrance_examination` (Assam, 666 rows, `TBD -> Yes` with `Ethical Issue`, `Missing source information` and `Data Quality Issue`; the record this was found for); other education records: `student_portuguese_performance`, `open_university_learning_analytics_dataset`, `early_learning_predictors`. No ENEM record before (grep: enem, INEP). External collections: not checked (the web search budget of the run was spent).
- Better data: found as better data for `student_performance_on_an_entrance_examination` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the INEP microdata page; the editions' Leia-me files (not read).
- Metric: none found (INEP defines no prediction task), so the fallback `rmse` on the score (or `log_loss` on score bands); inputs none.
- Risks for /add-dataset: race, sex and family income are features, and the Assam sibling carries `Ethical Issue` for caste, so the curator decides the same question for race here (SEL-1); the target (the mean of the objective tests, one area, or the essay) and absentees (no score for those who did not sit the exam); check in the chosen edition's Leia-me that scores and questionnaire answers still share one row per registrant (the Assessment notes that INEP removed identifying variables from recent releases; not verified here); one edition is millions of rows (a 1m cap).
- Priority: gap + (education thin), use case 0 (none named by the source), source + (INEP microdata with dictionaries), shape + (millions of rows, mixed types, yearly editions), risk - (the race column and the release format of recent editions).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `student_performance_on_an_entrance_examination`.
- as published: one row per registrant, millions per edition (roughly 3.9 million registrants in 2023, from memory, to check in the edition's Leia-me); registration and socioeconomic-questionnaire columns plus four ...; target: the candidate's ENEM score (mean of the objective tests, or one area such as mathematics; bands of it for a classification like the Assam record's four ...; access: open.
- Why: same task as the Assam record: predict a candidate's result in a national entrance examination from background known before the exam (sex, race, school type, parents' schooling and occupation, family income, state), the same kind of features as the Assam data (gender, caste, coaching, medium, parents' occupation); ...
- Adds: millions of candidates per year instead of 666 from one year in one Indian state, a documented government source instead of a UCI upload with missing source information, and many editions (temporal splits possible). Notes: INEP removed some identifying variables (e.g. the school code CO_ESCOLA) from recent releases; ...
