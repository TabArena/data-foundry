---
unique_name: bcf_lunghini_2019
name: 'QSPR models for bioconcentration factor (BCF): are they able to predict data of industrial interest? (data)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '2019'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.5281/zenodo.3228387
- https://doi.org/10.1080/1062936X.2019.1626278
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 1,333 chemicals with a fish logBCF compiled for a bioaccumulation model (Lunghini et al. 2019, Zenodo, CC BY 4.0), the regression form of `qsar_bioconcentration`'s quantity; the chemicals the two compilations share are to check.
- Source: Lunghini, Marcou, Azam, Patoux, Enrici, Bonachera, Horvath and Varnek, "QSPR models for bioconcentration factor (BCF): are they able to predict data of industrial interest?", SAR and QSAR in Environmental Research 30(7):507-524, 2019 (doi 10.1080/1062936X.2019.1626278); data Zenodo 3228387 (2019-05-24). As published: SI_BCFtrainset.xlsx, "a collection of 1129 chemical structures and CAS identifiers with their logBCF values extracted from various literature sources"; SI_BCFtestset.xlsx, "204 chemical structures for which the logBCF is considered of lower reliability"; SI_FullDataset_rawdata.csv, "15372 entries" (CASRN, tissue, duration, test organism, exposure type, steady state, response, media type, source, SMILES); 34 excluded outliers. The industrial data of the title is not among the four files.
- Use case: a regulatory or industrial chemist, before a fish bioconcentration test, decides whether a substance is likely bioaccumulative (abstract: "in the industrial context, these theoretical approaches may fail to predict BCF with reasonable accuracy"); fit direct; regime grouped on the Bemis-Murcko scaffold (SPLIT-31), as the other QSAR records.
- Siblings and duplicates: `qsar_bioconcentration` (Yes; Grisoni 2015/2016, 776 chemicals shipped, the class read from logBCF and logKOW): both merge public BCF compilations, so the shared chemicals by CAS are a PROV-6 question for the curator; `aquatic_toxicity_lunghini_consensus` (TBD -> Yes) is the same group's aquatic-toxicity data, another task. External collections: none found.
- Better data: found as better data for `qsar_bioconcentration`; no further search this round.
- Papers and pages: the paper (abstract read, full text paywalled); the Zenodo record; Bertato et al. 2022 (Toxics) reused the industrial benchmark.
- Metric: RMSE ("RMSE of 0.58 log BCF units", abstract), a headline number; whether the paper selects models by it was not read (MET-5); the fallback is `rmse` as well; inputs none.
- Risks for /add-dataset: overlap with Grisoni's chemicals (PROV-6); the 204 lower-reliability values, kept with a flag or dropped (USE-5); salts and stereoisomers collapse on 2D descriptors (LEAK-17); descriptors computed from the SMILES (CLEAN-24); the raw entries allow a per-test variant, a separate decision.
- Priority: gap 0 (chemistry, regression not thin), use case + (the paper names the regulatory and industrial decision), source + (paper and versioned deposit), shape + (1,333 chemicals, computed descriptors, scaffold groups), risk - (overlap with `qsar_bioconcentration`).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `qsar_bioconcentration`.
- as published: 1,129 training chemicals and 204 lower-reliability test chemicals with SMILES, CAS and logBCF (merged from public datasets, paper abstract), the raw 15,372 BCF entries (CASRN, tissue, duration, test ...; target: fish logBCF (regression); access: open (Zenodo, CC BY 4.0).
- Why: same quantity as the record (logBCF in fish, the record's alternative target and the input its classes are read from) and the same use case, chemicals as units with structure-derived features
- Adds: 1,333 chemicals against Grisoni's 1,056 (776 shipped), CC BY 4.0, plus per-test raw entries (organism, tissue, duration) that would allow a per-test variant; serves the regression form only (no logKOW, so no storage class). Both merge public BCF sets, so a check of shared chemicals by CAS is needed
