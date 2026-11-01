---
unique_name: pfizer_hitea_reaction_yield
name: 'Pfizer HiTEA: high-throughput experimentation reactions with yields'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Github
year: '2023'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/emmaking-smith/HiTEA
- https://doi.org/10.1038/s41557-023-01393-w
- https://doi.org/10.26434/chemrxiv-2022-hjnmr
- https://github.com/blaiszik/awesome-matchem-datasets
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10997498/
- '# the same reactions, deposited in the Open Reaction Database later (ord-data PR #188, 2024-07-12)'
- https://github.com/open-reaction-database/ord-data/blob/main/data/d9/ord_dataset-d92976309c3a48a3a64a4cf5e7048086.parquet
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: over 39,000 Pfizer medicinal-chemistry HTE reactions from more than ten years (Buchwald-Hartwig, Ullmann, hydrogenations and other classes) with UV-area yields, released with a Nature Chemistry paper; large real industrial data, but the source frames it as an explanatory analysis, it mixes reaction classes, and the file holds yield-derived columns.
- Source: King-Smith, Berritt, Bernier, Hou and co-authors (Pfizer and Cambridge), "Probing the chemical 'reactome' with high-throughput experimentation data", Nat. Chem. 2024 (received 2022-11-11, published 2024-01-02; doi 10.1038/s41557-023-01393-w, PMC10997498), preprint ChemRxiv 2022 (doi 10.26434/chemrxiv-2022-hjnmr). Data availability: "The full dataset is hosted on GitHub" (github.com/emmaking-smith/HiTEA, MIT, created 2022-10-16; `data/8_SEPT_APPROVED_full_dataset.csv`, 30 MB, committed 2023-09-08 as "full approved dataset for disclosure"; cleaned Buchwald, Ullmann and two hydrogenation subsets). Abstract: "39,000+ previously proprietary HTE reactions"; Main: "10 years of historical medicinal chemistry HTE data", over 350 target products. As published (header previewed): about 46 columns, among them `ReactionClass`, `SCREEN_ID`, `NOTEBOOK_ID`, `REACTION_ID`, reaction and product SMILES, `Product_Yield_PCT_Area_UV` (the yield), `Product_Yield_Mass_Ion_Count`, `Product_Selectivity`, solvent, temperature, time, catalysts, reactants and reagents with equivalents and SMILES, and `yie_react`, a string that begins with the yield.
- Use case: a medicinal chemist chooses catalyst, ligand, base and solvent for a new substrate before running a plate; fit approximate, since the paper says its framework "was not envisioned to predict or generalize any specific reaction property" and reads the data for chemical insight (SEL-3 holds through the field's use of HTE data for yield prediction, SEL-2; to confirm). Regime grouped by target product or screen, since the wells of one screen share a substrate (SPLIT-29).
- Siblings and duplicates: `pfizer_hte_39k` holds the same reactions through their later Open Reaction Database deposit (ord-data PR #188 "39k Pfizer dataset", 2024-07-12), proposed as a `Duplicate`; that ORD link is added here. The other reaction-yield records are other labs or screens: `buchwald_hartwig_yields`, `suzuki_miyaura_hte_yields` (Perera et al. 2018, also Pfizer, a flow screen: check that HiTEA does not include it), `amide_coupling_hte_47k`, `cn_coupling_hte_50k`, `ord_reaction_yields`, `uspto_reaction_yields` (PROV-7). External collections: the awesome-matchem-datasets list; ORD.
- Better data: from the curator's Zotero collection, items 191 and 99; no new search this run.
- Papers and pages: the Nat. Chem. paper (PMC full text: abstract, Main, Data availability); the HiTEA repository.
- Metric: none found: the paper fits random forests only as a diagnostic (out-of-bag accuracy, Supplementary Table 1), so the fallback `rmse` on the yield (MET-1, MET-8); inputs none.
- Risks for /add-dataset: drop `yie_react`, `Product_Yield_Mass_Ion_Count` and `Product_Selectivity`, which encode or are measured with the yield (LEAK-10); `SCREEN_ID`, `NOTEBOOK_ID` and `REACTION_ID` are ids, not features; one reaction class or all (the cleaned subsets hold a few thousand reactions each; USE-5); yields come from "the uncalibrated ratio of ultraviolet absorbances" and many are zero; molecules as SMILES go to descriptors (CLEAN-24); no run date in the header, so a temporal split would need one (to check).
- Priority: gap 0 (chemistry & material science and regression are not thin), use case 0 (explanatory source, approximate fit), source + (Nat. Chem. paper and the authors' repository), shape + (about 39,000 reactions, mixed categorical and numeric, grouped by screen), risk - (yield-derived columns and mixed reaction classes).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 191: "blaiszik/awesome-matchem-datasets"; the curator's Zotero collection, item 99: "blaiszik/awesome-matchem-datasets".
- as published: '39,000+ previously proprietary HTE reactions' (paper abstract, PMC10997498) covering cross-couplings, hydrogenations and chiral salt resolutions. data/8_SEPT_APPROVED_full_dataset.csv is 30.3 MB ...; target: Product_Yield_PCT_Area_UV: product yield as LC-UV area % (regression); zero vs non-zero yield as a binary alternative; access: open.
- Why: Real industrial experiments, not a designed academic full-factorial screen, released by Pfizer with a Nature Chemistry paper. | real industrial HTE results, including the 0% yields, released from a pharma ELN; dated, so a temporal split is possible
- Adds: Reaction-yield prediction, a chemistry task no record covers; far larger and more realistic than the Dreher-Doyle (3,955) and Suzuki (5,760) screens. Licence now confirmed: the data sits in the MIT-licensed repository, with no separate data licence (the awesome list says CC BY 4.0). Caveats: molecules as SMILES need ...
