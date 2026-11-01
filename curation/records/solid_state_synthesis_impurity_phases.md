---
unique_name: solid_state_synthesis_impurity_phases
name: Text-mined dataset of solid-state syntheses with impurity phases
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2025'
domain: chemistry & material science
problem_type: Binary Classification
source_links:
- https://doi.org/10.6084/m9.figshare.30423274
- https://doi.org/10.1038/s41597-025-06222-y
- https://doi.org/10.26434/chemrxiv-2025-jt69l
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 80,806 solid-state synthesis reactions text-mined from the literature with GPT-4o (Lee, Cruse, Baibakova, Ceder, Jain, Sci Data 2025), 18,869 with reported impurity phases; a large real record of outcomes, but the label is whether a paper reported an impurity and the LLM found it, not a measured purity.
- Source: Lee, Cruse, Baibakova, Ceder, Jain, "Text-mined dataset of solid-state syntheses with impurity phases using Large Language Model", Scientific Data (2025), doi 10.1038/s41597-025-06222-y, PMC12717135 (read); preprint ChemRxiv doi 10.26434/chemrxiv-2025-jt69l; data figshare doi 10.6084/m9.figshare.30423274, one JSON file (`SS_rxns_80806.json.gz`, 33.6 MB, not opened). Per record (Table 1): the source DOI, the target, precursors and impurity phases (formulas, compositions, Materials Project ids), the balanced reaction, and conditions (`heating_temperature`, `heating_time`, `heating_atmosphere`, `mixing_device`, `mixing_media`). Extraction: a MatBERT paragraph classifier, then a "few-shot LLM (gpt-4o-2024-05-13 with temperature = 0)"; publications with several synthesis protocols excluded. Validation on 98 hand-annotated reactions (Table 3): targets precision 0.90, recall 0.69; precursors 0.95/0.97; impurity phases 0.86/0.90 (21 cases).
- Use case: a solid-state chemist planning a synthesis predicts whether a recipe (precursors, temperature, time, atmosphere) will give impurity phases, to choose another route before running it. Fit approximate: the paper defines no prediction task (the dataset "validates expected thermodynamic trends" and finds hard cases), and the negative class is "no impurity phase reported". Regime grouped by target material or chemical system: recipes repeat across papers (Table 2: Bi2O3 + Fe2O3 to BiFeO3 is phase-pure in 107 of 221 reports).
- Siblings and duplicates: no record of this set (grep: impurity phase, solid-state synth, CederGroupHub, text-mined). Related text-mined records: `uspto_reaction_yields` (`TBD -> 2nd Tier`, priority 2, yields mined from patents: the precedent followed here), `melting_point_patents` (`TBD -> Yes`, priority 3), `zeosyn_zeolite_synthesis` (unscreened, zeolite synthesis outcomes). External collections: listed in `blaiszik/awesome-matchem-datasets` (a list, not a benchmark).
- Better data: from the curator's Zotero collection (items 99 and 191); no further search this round.
- Papers and pages: the Sci Data paper; Kononova et al., Sci Data 2019 (the earlier text-mined recipes, without purity); Thway et al. (82 chalcogenide syntheses, a decision tree at 61.5% test accuracy on impurity formation, cited in the paper).
- Metric: none (the paper trains no model), so the fallback `roc_auc` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: the label mixes reporting and extraction (an impurity not mentioned, or missed by the LLM, makes a "pure" row; target recall 0.69), a PROV-2 note and a possible `No Good Target` question for the curator; nested JSON to flatten and formulas to featurise (CLEAN); conditions often missing; the same reaction in several papers (group key from the target composition, SPLIT-24); publication bias toward syntheses that worked.
- Priority: gap 0 (chemistry and binary covered), use case 0 (the paper names no decision; approximate), source + (a Sci Data paper with a figshare release and a validated extraction), shape + (80,806 reactions, condition and composition features), risk - (a reported, LLM-extracted label).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 191: "blaiszik/awesome-matchem-datasets"; the curator's Zotero collection, item 99: "blaiszik/awesome-matchem-datasets".
- as published: 80,806 solid-state reactions (61,937 phase-pure, 18,869 with impurity or secondary phases) extracted by an LLM from the literature; one file SS_rxns_80806.json.gz (33.6 MB) with target, precursors ...; target: Whether the synthesis gives impurity or secondary phases (phase-pure vs not); access: open.
- Why: Large set of real reported outcomes linking precursor choice and temperature to purity, including partial failures. | large, real reported outcomes linking precursor choice and temperature to purity, including partial failures
- Adds: New against the first pass of this item; the same candidate as zotero_27 (item 191). Caveats: LLM extraction errors (PROV-2), nested JSON to flatten, publication bias in what papers report, recipes repeated across papers (group by target material). | no record. To check at screening: LLM extraction errors (PROV-2), ...
