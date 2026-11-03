---
unique_name: soil_compaction_proctor_mdd
name: Open dataset of soil compaction tests (Proctor maximum dry density and optimum moisture content from index properties)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Github
year: '2026'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/Sompote/open_compaction
- https://arxiv.org/abs/2609.03337
- https://doi.org/10.21203/rs.3.rs-11115086/v1
- https://doi.org/10.6084/m9.figshare.28681187
- https://doi.org/10.6084/m9.figshare.32955851
- https://doi.org/10.5281/zenodo.20737270
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: an open compilation of 4,877 laboratory Proctor tests from six public sources with per-record provenance, predicting maximum dry density from index properties and compaction energy; a long-standing geotechnical task at a size the field has not had, with few features and one source dominating.
- Source: Youwai, Phutthananon, Kongkitkul, "A Large Open Multi-Energy Corpus of Soil Compaction Tests, with Machine-Learning Baselines", arXiv 2609.03337 (3 September 2026; also Research Square doi 10.21203/rs.3.rs-11115086/v1); data on GitHub `Sompote/open_compaction` (v3.1.0, CC BY 4.0) with figshare and Zenodo deposits. As published (README read): `compaction_parameters.csv`, 4,877 tests complete in PI, fines, energy and Gs, from six public deposits and 47 open-access studies (LTPP Standard Data Release 39 gives 78%); `compaction_parameters_full.csv`, 7,272 rows with incomplete ones; `provenance.csv`, `sources.csv`, `references.csv`; columns LL, PL, PI, fines_pct, sand_pct, energy_kJm3, Gs, MDD_Mgm3, OMC_frac, group, record_id, source, test_standard. The paper's corpus is 2,854 tests from six sources and 162 provenance groups, after removing 11.8% of records that break the zero-air-voids condition (abstract).
- Use case: a geotechnical engineer at site investigation estimates the maximum dry density (and optimum moisture) of a soil from its index tests, to screen and rank borrow materials before running Proctor tests; README: "Intended use: preliminary screening and prioritisation only", "not a basis for accepting compacted fill or for any specification check". Fit direct. Regime grouped by provenance (`group`); README: "Use `GroupKFold` on `group` if you want an estimate of performance on a source the model has not seen", random splits answer "a different and easier question".
- Siblings and duplicates: no other compaction record (grep: compaction, proctor, LTPP). Other geotechnical records: `clay_10_7490_global_clay`, `tc304_clay_compression_index`, `tc304_rock_compressive_strength`, `sz_clay_shenzhen`, `tokyo_clay_airport_soil_properties`, `christchurch_lateral_spreading`, `soil_ksat_pedotransfer` (other properties and tasks, PROV-7). External collections: none known.
- Better data: from the curator's Zotero collection (item 264); no further search this round.
- Papers and pages: the arXiv paper (abstract read); the README's baselines (random five-fold MDD R^2 0.785-0.788 and MAE 0.075 Mg/m3; grouped folds about 0.70; source held out 0.48-0.49).
- Metric: R^2 throughout the paper, R^2 with MAE in the README, under three split protocols; no single criterion named, so the fallback `rmse` on MDD in Mg/m3 (MET-5, MET-8); inputs none (the group is the split key, not a scoring input).
- Risks for /add-dataset: which version ships (v3.1.0 with 4,877 tests against the paper's 2,854; one source's releases, PROV-6: take the maintained release and say why); OMC is a second outcome of the same test (one target per dataset; `OMC_frac` dropped from the MDD task, LEAK); LL is released but held out of the inputs since PI = LL - PL (keep two of the three, CLEAN); LTPP is 78% and, per the run's note, 97.5% of tests are standard Proctor, so energy varies little; the authors' zero-air-voids filter removed records (a note).
- Priority: gap 0 (environmental, regression and grouped covered), use case + (the README names the screening decision), source + (a paper and a versioned release with per-record provenance), shape + (4,877 tests, 6 inputs, 162 groups), risk - (one source dominates, a version to pick, few features).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 264: "A Large Open Multi-Energy Corpus of Soil Compaction Tests, with Machine-Learning Baselines".
- as published: one row per laboratory compaction test. The modelling file has 4,877 tests (v3.1.0, 8 sources) against 2,854 from 6 sources and 162 provenance groups in the paper. The wider pool has 7,272. Six ...; target: maximum dry density (Mg/m3), regression; optimum moisture content is the second target in the same file; access: open.
- Why: Real laboratory measurements with per-record provenance and an open licence. The predictors are all known before the Proctor test. The task is long-established in geotechnics, with four decades of published correlations. The paper reports a grouped or source-held-out split (TabPFN R2 0.82 random, 0.73 grouped, 0.52 ...
- Adds: A geotechnical and civil-engineering regression; the collection has no compaction or soil-mechanics record. It is far larger than the usual 100-400-specimen sets (e.g. Gunaydin 2009, 126 soils, zotero_04 item 42). Caveats: few features; LTPP dominates (78%) and 97.5% are standard Proctor; the split must be grouped by ...
