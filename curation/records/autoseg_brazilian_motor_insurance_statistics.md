---
unique_name: autoseg_brazilian_motor_insurance_statistics
name: AUTOSEG (SUSEP) Brazilian motor insurance statistics, semester files 2006-2020
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- Not Representative
tags:
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: GOV Website
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www2.susep.gov.br/menuestatistica/autoseg
- '# the page with the semester databases 2007-H2 to 2020-H2, as archived on 2026-04-11'
- http://web.archive.org/web/20260411231934/https://www2.susep.gov.br/menuestatistica/autoseg/principal.aspx
- '# SUSEP, Definições do AUTOSEG: the tables and variables (archived 2019-11-05)'
- http://web.archive.org/web/20191105000100/http://www2.susep.gov.br:80/menuestatistica/Autoseg/DEFINICOES_AUTOSEG.pdf
type_adapter_id: curation-record-v1
---

## Comments

**AI-FILLED, UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from the source pages, papers and data previews named below (measured where the notes say so). A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-20):** `TBD -> 2nd Tier`, priority 3: SUSEP's own definitions settle that the AUTOSEG rows
are rating cells, not policies, so the curator's rating-cell decision applies (2nd Tier with `Not Representative`,
policy question 4, Andrej, 2026-10-20); it is the origin of `brazilian_vehicle_insurance_autoseg_2011`.
- Source: SUSEP, the Brazilian insurance regulator, AUTOSEG v5.3, built from the insurers' semester submissions
  "referentes a apólices vigentes e sinistros ocorridos no período de análise" (hull cover, casco). Online queries
  from 2006-H2; downloadable databases for 2007-H2 to 2020-H2, 27 zip files on the page as archived on 2026-04-11,
  none later. As published (SUSEP, "Definições do AUTOSEG", archived 2019-11-05): per semester three main tables and
  nine code tables. `arq_casco_comp` holds exposure, premium, average sum insured, claim counts and indemnities for
  theft, partial collision, total loss, fire and other covers, "classificados pela chave Categoria
  Tarifária/Região/Modelo/Ano/Sexo/Faixa Etária"; `arq_casco3_comp` and `arq_casco4_comp` hold the same by postcode
  and by city, without sex and age. A row is a group of policies: "o conjunto de apólices incluídas na respectiva
  chave composta".
- Join: exposure and claims are columns of the same cell row, so nothing is joined. Whether the raw files also have
  claims in cells without exposure, as the CASdatasets 2011 copy has (15.4% of the claim amount), was not checked.
- Target and zeros: the indemnity total of a cell in a semester. On the 2011 copy it is 0 in 83.7% of cells, falling
  from 91% at exposure <= 0.5 to 8% above 100 vehicle-years, so the zero share mostly measures cell size. The zero is
  observed (no claim recorded in the cell); occurrence and amount are two mechanisms, summed over the cell.
- Use case: SUSEP names it: when AUTOSEG shipped on CD-ROM (until June 2005), "o público-alvo do Sistema AUTOSEG
  praticamente se restringia às companhias seguradoras, para subsidiar cálculos de tarifas"; an insurer setting next
  semester's tariff per cell. The fit is approximate for pricing a policy (cells), direct for a cell tariff. Regime
  temporal: train on past semesters, predict the next (SPLIT-6).
- Siblings and duplicates: `brazilian_vehicle_insurance_autoseg_2011` (CASdatasets `brvehins1`, CC Andrej: 2nd Tier,
  `Not Representative`) is a processed copy of the 2011 slice of this source (PROV-4, PROV-6), so the two should not
  both ship; this record is the origin and adds 26 semesters. `swedish_motorcycle_insurance_wasa` and
  `norwegian_automobile_insurance_norauto` got the same rating-cell call.
- Papers and pages: UFMG theses use the files (da Mata 2023, Sec. 2.1: "links para download dos bancos de dados
  semestrais, organizados em três tabelas principais e nove tabelas auxiliares"; de Carvalho 2021, Sec. 2.1, 70 cells
  of one car model for 2019).
- Risks for /add-dataset: SUSEP's site refused connections from here again (2026-10-20), and the Wayback Machine has
  the page and the definitions but no zip, so no file was opened; which cover is the target (theft does not scale like
  collision); claims in cells without exposure; FIPE model codes and regions may change over 14 years.
- Priority: gap 0, use case + (SUSEP names tariff calculation), source + (the regulator's definitions), shape + (27
  semesters, many cells, mixed features), risk - (cells, not policies; files unreachable from here).

**Assessment (AI, 2026-10-30):** suggested call for policy question 3 of the zero-inflated review, where Andrej asked
for a call per dataset from its references and the domain's practice instead of one convention for the family (the
shared reasoning: a time exposure or a sum insured is a feature, and a rating-cell table weights the metric by its
exposure; negative amounts that are recoveries become 0; the source's metric first, else the normalized Gini as a
context metric, since RMSE on raw amounts follows a few large claims and a Tweedie or Poisson deviance needs positive
predictions; MET-10 as amended on 2026-11-02 (Andrej) later declined a family-wide metric, so each table's metric is
decided on its own); the curator
has the call.
- The 2nd Tier with `Not Representative` stays: rows are rating cells.
- If it is built: the target is the cell's indemnity per vehicle-year (a pure premium), the hull covers summed, and the
  cell's exposure weights the metric (a scoring column, MET-2). That is how rating-cell tables are modelled (Ohlsson and
  Johansson's GLM book, the source of `swedish_motorcycle_insurance_wasa`, weights by duration), and it removes the
  growth of the target with cell size, though the rows stay cells.
- Negative amounts: not known (no file opened).
- Metric: an exposure-weighted `rmse` on the pure premium (custom, MET-13), or the fallback.

**Assessment (AI, 2026-10-30):** to the curator's question ("Now is this a real predictive task or not?"): real, at the
level of a rating cell. SUSEP names the use (insurers took AUTOSEG "para subsidiar cálculos de tarifas"), and predicting
next semester's claim cost per vehicle-year of a cell from its keys (tariff category, region, model, model year, sex,
age band) is the cell tariff of actuarial practice. It is not the pricing of one policy, which is what the curator's
rating-cell call of 2026-10-20 weighed (2nd Tier with `Not Representative` on `swedish_motorcycle_insurance_wasa` and
`brazilian_vehicle_insurance_autoseg_2011`). Recommend 2nd Tier by that call; if cell tariffs become a task of their
own, this is the rating-cell record to take (27 semesters, a temporal split), with the per-exposure target suggested
above. The files still could not be opened from here.

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 3 (the AI screening had `TBD -> 2nd Tier`, priority 3;
zero-inflated screening review page, after the AI's answer to the curator's question).

## Reference

SUSEP, AUTOSEG - Sistema de Estatísticas de Automóveis, version 5.3, semester databases 2007-H2 to 2020-H2; "Definições do AUTOSEG" (tables and variables). https://www2.susep.gov.br/menuestatistica/autoseg

Lead: zero-inflated screening review, policy question 6 (curator's go, Andrej, 2026-10-20); sibling of `brazilian_vehicle_insurance_autoseg_2011`.
