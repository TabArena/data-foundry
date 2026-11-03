---
unique_name: sinalize_sin_transformer_forced_outages
name: 'SINALIZE: forced outages, maintenance, registry and climate exposure of power transformers in the Brazilian National Interconnected System (SIN)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2026'
required_split:
- Temporal (NON-IID)
source_links:
- https://doi.org/10.5281/zenodo.21010260
- https://zenodo.org/records/22303287
- https://zenodo.org/records/21010261
- https://dados.ons.org.br/dataset/capacidade-transformacao
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a 2026 Zenodo release (UFRJ, CC BY 4.0) of 18,431 forced and 14,676 maintenance outages of 1,698 power transformers of Brazil's interconnected grid (January 2020 to July 2026), with a registry and daily climate per grid cell, published for "failure prediction and predictive maintenance"; the target and its period are ours to build, and where the event table comes from is not stated.
- Source: Rodrigo Guimaraes (Universidade Federal do Rio de Janeiro), "SINALIZE - Dataset para previsão de falhas em transformadores de potencia e frequencia do SIN", Zenodo, v2 2026-09-04 (doi 10.5281/zenodo.22303287; concept doi 10.5281/zenodo.21010260; v1 2026-06-28, doi 10.5281/zenodo.21010261, 2023-2025 with 15-minute load series, 1.2 GB). The description: "This dataset supports research on failure prediction and predictive maintenance for power transformers of the Brazilian National Interconnected System (SIN), operated by the National Electric System Operator (ONS). It covers the period from January 2020 to July 2026 and was fully de-identified before publication." As published (DICIONARIO.md and file previews, 2026-10-31): falhas.csv (18,431 forced outages: equipment, start, end, minutes, outage type, cause origin, electrical nature, cause nature, reclosing type), manutencao.csv (14,676 maintenance outages: equipment, start, end, minutes), transformadores.csv (1,698 units, 13 columns: commercial operation date, substation arrangement, base and winding voltages, operator and owner pseudonyms, number of units, climate cell, function, transformer type), clima/ (345 daily NASA POWER series, one per 0.5 x 0.625 degree cell); semicolon-separated, no header; equipment, agents and cells pseudonymised ("The correspondence table is not published"). "A companion paper describing the Sinalize tool, the strategic analysis universe, and the honest temporal validation protocol is under preparation."
- Use case: a transmission owner's or ONS's asset manager, at the start of a period, decides which transformers to inspect or maintain first from their risk of a forced outage in the period (the release names "failure prediction and predictive maintenance"); fit approximate until a horizon is fixed (USE-8: no stated horizon). Regime temporal (the release names a temporal validation protocol), with the transformer as the entity (SPLIT-13).
- Siblings and duplicates: `power_grid` (`No`, `AHDS`), the record this was found next to; `distribution_transformers_at_cauca_department` (`Yes`; distribution transformers of one Colombian department, another source and scale); `eaglei_county_outages_weather_warnings` (`TBD -> 2nd Tier`, county outages, another task). ONS's open-data portal (dados.ons.org.br, catalogue of 88 datasets read 2026-10-31) publishes the transformer registry (capacidade-transformacao, current state only) and monthly availability indicators aggregated by function and voltage (ind_disponibilidade_ft_trlt), but no per-event outage table, so the origin of falhas.csv is not stated (PROV-2). External collections: none found.
- Better data: found as a related task next to `power_grid` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the Zenodo records (v1, v2); the ONS open-data catalogue; no paper yet.
- Metric: none found (no paper; the release scores nothing), so the fallback `roc_auc` for "a forced outage in the next period" (MET-1, MET-8), or `rmse` on a count if the curator prefers the count; inputs: the period and the transformer for the split.
- Risks for /add-dataset: the target and horizon are ours (one row per transformer and period; `Needs extensive data wrangling`: join the registry, the outage and maintenance histories and the climate by cell); many forced outages have an external origin and hit several transformers at the same minute (the preview shows five units at 2021-10-30 05:19, "Externa", "Bifásica", "FUGITIVO"): decide whether the target counts only internal failures (USE-5); a unit's past outages are legitimate history under a temporal split (LEAK-34), but the task must beat each unit's naive outage rate (SEL-11, TP-10); maintenance after the period start is not known then (LEAK-10); ask the author where the events come from (PROV-2); a single-author deposit whose paper is in preparation.
- Priority: gap 0 (industry, binary and temporal not thin), use case 0 (the release names the purpose, not the actor), source + (a documented release with a data dictionary), shape + (1,698 units over 6.5 years, mixed types, temporal), risk − (a target to build, events of unstated origin).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `power_grid`.
- as published: v2 (2026-09-04, CC BY 4.0): 1,698 power transformers (registry, 13 columns: commercial operation date, substation arrangement, base and winding voltages, operator and owner pseudonyms, number of ...; target: Whether a transformer has a forced outage (failure) in the next period, built per transformer and period from falhas.csv; alternatively the count of forced ...; access: open.
- Why: power_grid is generated (grid_status from randomly drawn loads, voltage and frequency, per its Kaggle description), so better data would be real labelled grid faults with measured operating states; those exist only as PMU or waveform event libraries (ORNL GESL, LBNL micro-PMU with 26 events), time series and not ...
- Adds: A real grid-failure task with a temporal regime over 6.5 years of events. It may also be better data for distribution_transformers_at_cauca_department, which has only two yearly labels, though that record covers distribution transformers in one Colombian department. Risks: the per-event outage table cannot be traced ...
