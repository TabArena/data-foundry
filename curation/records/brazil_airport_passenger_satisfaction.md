---
unique_name: brazil_airport_passenger_satisfaction
name: Pesquisa de Satisfacao do Passageiro (Indicadores de Satisfacao do Passageiro - Processos e Servicos Aeroportuarios - Aeroportos Principais)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: GOV Website
source_links:
- https://dados.transportes.gov.br/dataset/pesquisa-de-satisfacao-do-passageiro-em-aeroportos
- https://dados.transportes.gov.br/dataset/e2fdb29b-7b7d-42f9-b1a6-ff3b881ef1ef/resource/d338dafe-213f-4857-a08e-225b65841ba2/download/dicionario-de-dados.ods
- https://dados.transportes.gov.br/dataset/pesquisa-de-satisfacao-do-passageiro-em-aeroportos-regionais
- https://doi.org/10.47456/bjpe.v10i2.44374
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the Brazilian ministry's official airport passenger satisfaction survey, 2013-2026 in quarterly files with a dictionary and methodology, the real counterpart of the generated airline satisfaction uploads; whether an overall rating explained by the same interview's item ratings is a prediction task is the open question (SEL-3).
- Source: Secretaria Nacional de Aviação Civil (SAC), Ministério de Portos e Aeroportos, on dados.transportes.gov.br, "Indicadores de Satisfação do Passageiro - Processos e Serviços Aeroportuários Oferecidos - Aeroportos Principais" (portal entry created 2020-08-26, public domain): face-to-face interviews "nas salas de embarque e desembarque dos aeroportos" with domestic and international passengers, sampled by passenger flow (95% confidence, 5% maximum error) on the 20 busiest days of the month. As published: one ODS for 2013-2019, one for Q1 2020, quarterly CSV or XLSX files from Q1 2021 to Q2 2026 (no survey April-July 2021; only March in Q1 2023 and October in Q4 2022; "a pesquisa foi suspensa em meados de junho de 2026" for budget reasons), a data dictionary with one tab per methodology, and methodology documents of 2018 and 2020. Per the run's assessment, about 45 columns until 2019 and 96 from 2020 (airport, terminal, airline, flight, about 60 ratings 1-5, passenger profile); not recounted. Target: the overall satisfaction (SATISFACAO GERAL), 1-5.
- Use case: the airport operator and SAC, each quarter, find the passengers and processes that drive dissatisfaction and decide where to act; fit approximate: target and features come from the same interview, so the model explains a rating rather than predicting one before it is known (SEL-3, USE-2 open; the curator on `us_airline_passenger_satisfaction`: "Survey data, but prediction task seems very reasonable"). Regime temporal (quarterly waves; de Oliveira et al. 2024 trained on 2017-2022 and tested on 2023), airports as a possible group.
- Siblings and duplicates: `us_airline_passenger_satisfaction` (`TBD -> 2nd Tier`; its ratings are generated, CC 2026-10-01) and `customer_satisfaction_in_airline` (`No (Retired)`, AHDS), whose audit used this survey as the real reference (no rating pair agrees on more than 68% of rows); `antt_interstate_bus_ticket_sales` (same portal, another task). The regional-airports survey (https://dados.transportes.gov.br/dataset/pesquisa-de-satisfacao-do-passageiro-em-aeroportos-regionais) is a cut of the same programme (PROV-6). No duplicate (grep for satisfacao, passageiro, dados.transportes). External collections: none found.
- Better data: from the run's search, found as better data for `us_airline_passenger_satisfaction`; no further search this round.
- Papers and pages: de Oliveira, Lima, dos Santos, "Utilização de modelos de aprendizado de máquina para a classificação da satisfação de usuários nos aeroportos do Brasil", Brazilian Journal of Production Engineering 10(2), 2024 (doi 10.47456/bjpe.v10i2.44374): KNN, naive Bayes, decision tree and random forest on this survey.
- Metric: none found as one choice (the BJPE abstract names no metric: "para melhorar os resultados das métricas"; the full text was not read); fallback `roc_auc` for satisfied (4-5) against not, or `rmse` if the 1-5 score ships (MET-5, MET-8).
- Risks for /add-dataset: SEL-3 and USE-2 (the curator's call); a field giving the reason for an overall score below 4 restates the target (named in the run's assessment, LEAK-10); two methodologies with different columns, so one era per dataset; partial quarters; the binary cut (USE-5); free-text fields if any (SEL-12).
- Priority: gap 0, use case 0 (SAC names monitoring, no prediction decision), source + (a ministry with a dictionary and methodology), shape + (many thousands of interviews per year, ratings, profile and dates), risk - (target and features from one interview).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `us_airline_passenger_satisfaction`.
- as published: one row per passenger interviewed in the boarding and arrival halls of the 20 main airports (87% of scheduled passengers); 2013-2019 in one consolidated ODS (about 45 columns: 36 ratings 1-5, ...; target: SATISFACAO GERAL: the passenger's overall satisfaction with the airport, 1-5 (binary satisfied >= 4 vs not, like the record's satisfied vs neutral or ...; access: open.
- Why: the same quantity as the record (a passenger's overall satisfaction from her ratings of the services along the trip and her travel profile), measured in an official, documented survey; the record's ratings were shown to be generated (CC 2026-10-01 on customer_satisfaction_in_airline, which used this survey as its ...
- Adds: real and traceable data (PROV-1, PROV-3) against an untraceable generated upload; public domain; a data dictionary and methodology documents (2018, 2020); hundreds of thousands of interviews over 2013-2026 against 129,880 generated rows; dates, airports and airlines allow temporal or grouped splits. Risks for ...
