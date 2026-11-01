---
unique_name: aquatic_toxicity_lunghini_consensus
name: 'Consensus QSAR models estimating acute aquatic toxicity for three trophic levels organisms: Algae, Daphnia and Fish (data)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2020'
domain: chemistry & material science
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.3708082
- https://doi.org/10.1080/1062936X.2020.1797872
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 3,680 public compounds with acute toxicity values for algae (72-h EC50), Daphnia (48-h EC50) and fish (96-h LC50), merged from public sources by Strasbourg and Solvay; a larger form of the two UCI aquatic toxicity tasks, with the structure as the only input.
- Source: Lunghini, Marcou, Azam, Enrici, Van Miert, Varnek (Université de Strasbourg, Solvay), Zenodo doi 10.5281/zenodo.3708082 (2020-03-12, CC BY 4.0): "3680 public unique compounds annotated by, at least, one experimental value for the given endpoint"; companion article "Consensus QSAR models estimating acute toxicity to aquatic organisms from different trophic levels: algae, Daphnia and fish", SAR and QSAR in Environmental Research 31(9):655-675, 2020 (doi 10.1080/1062936X.2020.1797872; not opened, 403). As published: one SDF (`MergedEndpoints.sdf`, 6.3 MB) with canonical SMILES, CAS number, the data sources (the preview shows NITE, VEGA, ECOTOX, OASIS and a "Literature set"), the endpoints present, and per endpoint the value in mg/L and as pEC50/pLC50 (the negative log of mmol/L, checked on the first record). The counts per endpoint and how repeated values were combined are not on the page.
- Use case: a hazard assessor at a chemical maker or a regulator estimates the acute aquatic toxicity of a new substance before testing, for classification and labelling; the Zenodo page names no actor (the industrial interest is Solvay's), fit approximate; regime not set by the source (grouped by scaffold or IID by compound, for /add-dataset).
- Siblings and duplicates: `qsar_aquatic_toxicity` (`Yes (Disagreement)`, 546 Daphnia chemicals) and `qsar_fish_toxicity` (`Yes`, 908 fathead minnow chemicals) draw on the same public pools, so many of their chemicals likely recur here (another source, its own record, PROV-4; check the overlap by CAS); `adore_aquatic_toxicity` (unscreened, per-test entries from ECOTOX), `fish_toxicity` (`No`), `bcf_lunghini_2019` (the same group, another endpoint). External collections: none found.
- Better data: found as better data for `qsar_aquatic_toxicity` and `qsar_fish_toxicity`; no further search this round.
- Papers and pages: the Zenodo record; the SAR QSAR Environ Res article.
- Metric: not read (the article was not reachable; the Zenodo page says only that the SVM models were validated following OECD principles), so the fallback `rmse` on the log scale (MET-8), to check against the article's ranked criterion; inputs none.
- Risks for /add-dataset: three endpoints, so one task per endpoint or one chosen (the per-endpoint counts decide whether algae is too small, TP-5); the features must be computed from the SMILES and the structures standardised (CLEAN-24; LEAK-17 for duplicate structures); the combination of repeated measurements is not documented.
- Priority: gap 0 (chemistry & material science and regression are not thin), use case 0 (no decision named on the page), source + (the authors' deposit with a peer-reviewed article), shape + (3,680 compounds).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `qsar_aquatic_toxicity`, `qsar_fish_toxicity`.
- as published: 3,680 unique public compounds, each with at least one of three endpoints (Daphnia 48-h EC50, fish 96-h LC50, algae 72-h EC50), one value per compound and endpoint in log and mg/L; one SDF with ...; target: Daphnia 48-h pEC50 (immobilization) or fish 96-h pLC50 per compound; access: open (CC BY 4.0).
- Why: Same target and unit (one toxicity value per chemical) as qsar_aquatic_toxicity (Daphnia magna 48 h) and qsar_fish_toxicity (fish 96 h), structure given
- Adds: One aggregated value per chemical (the shape of the UCI tasks, unlike ADORE's per-test entries) over up to 3,680 compounds against 546 and 908; structures given; open CC BY 4.0
