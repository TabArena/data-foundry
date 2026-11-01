---
unique_name: pfizer_hte_39k
name: 'Pfizer high-throughput experimentation archive: 39,000+ reactions (the ''reactome'' paper)'
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
source_links:
- https://doi.org/10.1038/s41557-023-01393-w
- https://github.com/open-reaction-database/ord-data/blob/main/data/d9/ord_dataset-d92976309c3a48a3a64a4cf5e7048086.parquet
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10997498/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): the Open Reaction Database deposit of the Pfizer HTE reactions released with King-Smith et al. (Nat. Chem. 2024); `pfizer_hitea_reaction_yield` records the same data from its first publication, the authors' GitHub repository.
- Source: King-Smith et al., "Probing the chemical 'reactome' with high-throughput experimentation data", Nat. Chem. 2024 (doi 10.1038/s41557-023-01393-w, this record's first link; PMC10997498): "39,000+ previously proprietary HTE reactions"; Data availability: "The full dataset is hosted on GitHub" (github.com/emmaking-smith/HiTEA, `data/8_SEPT_APPROVED_full_dataset.csv`, committed 2023-09-08 as "full approved dataset for disclosure"). This record's second link, ORD `ord_dataset-d92976309c3a48a3a64a4cf5e7048086`, entered ord-data with PR #188 "39k Pfizer dataset" (2024-07-11, merged as #189 on 2024-07-12): "39k reaction dataset from https://doi.org/10.1038/s41557-023-01393-w. This is a Pfizer dataset which was previously proprietary but was published earlier in 2024"; "Original dataset preparation by emmaking-smith", with solvent and reagent names split into components and SMILES added.
- Why a duplicate: both records end at the same original source, the HiTEA paper and its repository (PROV-4, PROV-8); the ORD copy re-encodes the same reactions in ORD's schema and adds no task. The per-class tables this record proposes (one reaction class such as Buchwald-Hartwig) are cuts of the same file (PROV-6), and the repository already ships cleaned Buchwald, Ullmann and hydrogenation subsets. ORD's added reagent SMILES can serve the canonical record's build as a cleaner encoding of the same rows.
- Siblings and duplicates: the record to keep is `pfizer_hitea_reaction_yield` (`TBD -> Yes`, priority 2), which now lists this ORD deposit among its links. The other reaction-yield records (`buchwald_hartwig_yields`, `suzuki_miyaura_hte_yields`, `amide_coupling_hte_47k`, `cn_coupling_hte_50k`, `ord_reaction_yields`, `uspto_reaction_yields`) hold other screens. External collections: ORD; the awesome-chemistry-datasets list.
- Better data: found through the awesome-chemistry-datasets list (and the curator's Zotero collection, item 150); no new search this run.
- Reject check (AI, 2026-10-31): stands. ord-data PR #188 '39k Pfizer dataset': '39k reaction dataset from https://doi.org/10.1038/s41557-023-01393-w. This is a Pfizer dataset which was previously proprietary ...' and 'Original dataset preparation by @emmaking-smith' (https://github.com/open-reaction-database/ord-data/pull/188). These are the HiTEA repository's reactions, which pfizer_hitea_reaction_yield records from the first publication, re-encoded with reagent SMILES. The ORD link is already on the survivor, and per-class tables are cuts (PROV-6). One fact to fix in the block: the GitHub API gives PR #188 itself as merged on 2024-07-11, not '#189 on 2024-07-12'.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 150: "Interpretable Multiple Myeloma Prognosis with Observational Medical Outcomes Partnership ...".
- as published: 39,347 reactions in ORD, previously proprietary Pfizer HTE covering cross-couplings, hydrogenations and chiral salt resolutions; target: reaction outcome per HTE well (yield or conversion; per reaction class, to check); access: open.
- Why: large real industrial HTE data, disclosed for exactly this kind of analysis
- Adds: breadth across reaction classes. Risks: heterogeneous outcomes across classes, so a record takes one class (e.g. Buchwald-Hartwig) as its own table; outcome definitions to check
