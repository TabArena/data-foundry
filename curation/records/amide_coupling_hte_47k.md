---
unique_name: amide_coupling_hte_47k
name: 'Amide coupling HTE: 632 amine-acid pairs under 95 conditions (AIChemEco 47k)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.1039/d5sc03364k
- https://github.com/aichemeco/amide_coupling
- https://github.com/open-reaction-database/ord-data/blob/main/data/47/ord_dataset-47eaacc46c3a4487bbdf99adb1a15e41.parquet
- https://doi.org/10.26434/chemrxiv-2024-tzsnq
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and papers, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: about 47,000 measured amide-coupling yields from one HTE platform, 632 amine-acid pairs picked for diversity under up to 95 conditions, with the paper's own substrate-novelty test; a real condition-choice task with enough pairs for a grouped split.
- Source: Zhang, Lin, Yang, Kong, Yu and Liao 2025, "Intermediate knowledge enhanced the performance of the amide coupling yield prediction model", Chem Sci 16:11809 (doi 10.1039/d5sc03364k, online 2025-06-05, CC BY-NC 3.0; Guangzhou National Laboratory, Guangzhou Medical University and AIChemEco Inc.; preprint ChemRxiv doi 10.26434/chemrxiv-2024-tzsnq). "Data availability https://www.github.com/aichemeco/amide_coupling/tree/main" (repository under MIT). As published: `all_HTE_with_codnition.csv`, "all 47,000 HTE reaction data for amide coupling reaction using 95 reaction conditions" (README: amine, acid and product SMILES and a condition id 1-95), six single-condition files, a substrate workbook and a USPTO amide subset. "a final dataset of 632 products corresponding to 632 unique substrate pairs, which include a total of 70 amines and 66 acids": 447 picked by sampling a virtual space of buyable substrates, 186 added by experts. Yields from "UPLC, MS, and NMR", with "internal standards for accurate yield measurement"; "more than 47 000 yield data were collected, excluding those discarded data, where overlapping of chromatography peaks and difficulty in NMR analysis usually result in the failure to obtain the corresponding yield data" (Europe PMC full text, PMC12139636). A copy sits in the Open Reaction Database (`ord_dataset-47eaacc46c3a4487bbdf99adb1a15e41`, 8 MB parquet, not opened).
- Use case: a medicinal chemist, before running an amide coupling on a new amine-acid pair, picks the coupling reagent and conditions ("condition recommendation remains a challenging issue due to the broad condition space"; "This strict testing better reflects real-world applications where chemists need to predict reaction yields for novel substrate pairs"); fit direct. Regime grouped by substrate pair, the paper's "full substrate novelty" test: a random split lets a model see the same pair under other conditions (SPLIT-29, USE-10).
- Siblings and duplicates: no other amide-coupling HTE record. The other reaction-yield records of this run, `buchwald_hartwig_yields`, `cn_coupling_hte_50k`, `suzuki_miyaura_hte_yields`, `pfizer_hte_39k`, `pfizer_hitea_reaction_yield`, `uspto_reaction_yields`, `ord_reaction_yields` and `catechol_solvent_selection_yields`, cover other reactions or labs (PROV-7). The ORD deposit is a copy of this source. External collections: Open Reaction Database; awesome-chemistry-datasets.
- Better data: from the awesome-chemistry-datasets list and the curator's Zotero collection (item 150); no further search this round.
- Papers and pages: Zhang et al. 2025 (the data); the ChemRxiv preprint (2024); Liu, Moroz and Isayev 2023 on amide-coupling yields from literature data (Chem Sci, PMC10566507) as related work.
- Metric: Table 1 ("Model evaluation on the HTE dataset") and the abstract report R2, MAE and RMSE side by side for each split, none named as the criterion (MET-5), so the fallback `rmse` on the yield in percent; inputs none.
- Risks for /add-dataset: the inputs are SMILES and a condition id, so descriptors are computed from the structures (CLEAN-24) and the conditions decoded from the workbook (reagent, base, additive, CLEAN-12); the "intermediate knowledge" of the paper is a SMARTS-built structure, not a measurement, so no leak; wells dropped for unreadable chromatograms are missing not at random, and only DMF-soluble substrates were kept ("substrates with poor solubility in DMF were systematically excluded"), a note for the fit (USE-8); one lab's platform.
- Priority: gap 0 (chemistry & material science, regression and grouped are not thin), use case +, source +, shape + (about 47,000 rows, 632 pairs, 95 conditions), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 150: "Interpretable Multiple Myeloma Prognosis with Observational Medical Outcomes Partnership ...".
- as published: 47,015 reactions: 70 amines and 66 acids giving 632 product pairs (447 chosen by diversity sampling, 186 by experts), each under up to 95 coupling conditions, run on an in-house HTE platform; target: measured yield of the amide coupling; access: open.
- Why: the most common medicinal-chemistry reaction; large, measured, substrates sampled for diversity; the paper scores random, partial and full substrate-novelty splits
- Adds: 632 substrate pairs make a grouped split by substrate meaningful, unlike the 8-15 pairs of the cross-coupling sets. Risks: one company's platform; check the licence of the GitHub copy
