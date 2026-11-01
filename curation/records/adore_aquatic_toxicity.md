---
unique_name: adore_aquatic_toxicity
name: 'ADORE: A benchmark dataset for machine learning in ecotoxicology'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
original_source: Other
year: '2023'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.25678/0008C9
- https://doi.org/10.1038/s41597-023-02612-2
- https://renkulab.io/gitlab/mltox/adore
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: an expert-curated ML benchmark of acute aquatic toxicity from US EPA ECOTOX (33,448 tests on 2,408 chemicals and 203 species), the endpoints of `qsar_fish_toxicity` and `qsar_aquatic_toxicity` with about twice their chemicals, published with splits by chemical.
- Source: Schür, Gasser, Perez-Cruz, Schirmer, Baity-Jesi, "A benchmark dataset for machine learning in ecotoxicology", Scientific Data 10:718, 2023-10-18 (doi 10.1038/s41597-023-02612-2, read in full on Europe PMC, PMC10584858); data in Eawag's ERIC repository (doi 10.25678/0008C9), code at renkulab.io/gitlab/mltox/adore; built from the ECOTOX database (September 2022 release, per the scout). As published: fish 26,114 entries (140 species, 1,905 chemicals), crustaceans 6,630 (17 species, 1,444 chemicals), algae 704 (46 species, 174 chemicals); target the LC50 or EC50 in mg/L (molar values derived), modelled as log10; features: chemical properties (molecular weight, water solubility, logP, pKa, atom and ring counts), six molecular representations (MACCS, PubChem, Morgan, ToxPrint, Mordred, mol2vec), species traits (AmP ecology and life history, phylogenetic distances) and test conditions (media type, observation duration, exposure and concentration type).
- Use case: a regulatory hazard assessor estimates a chemical's acute toxicity to a species instead of running the animal test ("Regulatory hazard assessment relies on extensive animal testing"); fit direct; regime grouped by chemical, the authors' recommendation ("suggest to split by occurrence of chemical compounds"; they advise against the random split as overestimating performance), so a new chemical is the unit of generalisation.
- Siblings and duplicates: `qsar_fish_toxicity` (Yes; 908 chemicals, fathead minnow 96-h LC50, Cassotti 2015) and `qsar_aquatic_toxicity` (Yes (Disagreement); 546 chemicals, Daphnia magna 48-h, Cassotti 2014) hold the same endpoints from other compilations: overlapping chemicals, different sources, so not duplicates (PROV-4); `aquatic_toxicity_lunghini_consensus` (a candidate of this run: 3,680 compounds, one value per compound and endpoint) is the closest alternative. External collections: none found.
- Better data: found as better data for `qsar_aquatic_toxicity` and `qsar_fish_toxicity`; no further search this round.
- Papers and pages: the data paper; the ADORE repository; later work on it, for example "Multimodal Integration of Chemical and Biological Descriptors for Cross-Species Prediction of Fish Acute Toxicity" (ES&T 2026, doi 10.1021/acs.est.5c12494; listed by Semantic Scholar, not read).
- Metric: none found (the paper names no metric for its challenges, read in full), so the fallback `rmse` on log10 of the concentration (MET-1, MET-11); inputs: the chemical as the group, which ships.
- Risks for /add-dataset: one dataset or several: the paper defines challenges from all taxa down to single species (fish, Daphnia magna, rainbow trout), so pick the cut that matches the use case and say why (PROV-6 among the cuts); repeated tests of one chemical and species are all kept ("included all such data points"), so group by chemical and decide on aggregation (LEAK-17); test conditions are inputs only where the assessor sets them (USE-6); the representations are the authors' computations from the structure (CLEAN-24: take theirs or compute from SMILES); species traits repeat per species.
- Priority: gap 0 (chemistry & material science, regression and grouped not thin), use case +, source +, shape + (33,448 entries, 2,408 chemicals, mixed features, grouped structure), risk - (the unit and the cut are open).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `qsar_aquatic_toxicity`, `qsar_fish_toxicity`.
- as published: 33,448 test entries on 2,408 chemicals: fish 26,114 entries (140 species, 1,905 chemicals), crustaceans 6,630 (17 species, 1,444 chemicals), algae 704 (46 species, 174 chemicals); single-species ...; target: acute LC50/EC50 (mg/L and mol/L), exposure up to 96 h: fish 96-h LC50, crustaceans 48-h EC50/LC50, algae growth EC50; access: open (Eawag open data; article CC BY 4.0).
- Why: Same target as qsar_fish_toxicity (fish 96-h LC50, fathead minnow included) and qsar_aquatic_toxicity (Daphnia magna 48-h LC50/EC50), the chemical as unit, structure-based features known before the test
- Adds: About twice the fish chemicals (1,905 against 908) and 2.6 times the crustacean chemicals (1,444 against 546), newer (ECOTOX 2022), expert-curated with structures, standard representations and splits by chemical; caveat: several test entries per chemical (species, repeats), so aggregation or grouping by chemical is ...
