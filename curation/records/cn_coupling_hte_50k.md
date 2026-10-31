---
unique_name: cn_coupling_hte_50k
name: 50,688 Pd-, Ni- and Cu-catalysed C-N coupling reactions (Cernak group ultra-HTE)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
domain: chemistry & material science
problem_type: Regression
source_links:
- https://doi.org/10.1021/jacs.6c05959
- https://github.com/open-reaction-database/ord-data/blob/main/data/80/ord_dataset-805ad863feef48579d95d86a728035f4.parquet
- https://github.com/cernak-lab/cernakHTE
- http://pharos.cernaklab.com/
- https://doi.org/10.21203/rs.3.rs-7603680/v1
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 50,688 C-N coupling reactions under Pd, Ni and Cu catalysis from one ultra-HTE campaign, deposited open in the Open Reaction Database; the Buchwald-Hartwig yield task at about 13 times the size, with few substrates.
- Source: Das, Zhang, Tan, Abdelalim, Lu, Mauro, Regan and Cernak, "A 50,688-Reaction Data Set Reveals General Ligands and Mechanistic Diversity in C–N Couplings", J. Am. Chem. Soc. 148(25):26401-26412 (online 2026-06-17, doi 10.1021/jacs.6c05959); preprint "Metal counterfactuals reveal ligand generalizability and mechanistic diversity in C–N couplings", Research Square, 2025-09-26 (doi 10.21203/rs.3.rs-7603680/v1), with the data then on a Globus link (cernakHTE README: "We have deposited all data on the Globus link found in the manuscript"); the Open Reaction Database deposit `ord_dataset-805ad863feef48579d95d86a728035f4` (ord-data PR #243 "Cernak 50k CN Coupling", committed 2026-06-19; a 5.2 MB parquet; the PR summary says 50,687 reactions); code on GitHub cernak-lab/cernakHTE (no licence; "Provided here is the code used, without the data"). The abstract (Europe PMC, summarised): Pd, Ni and Cu conditions compared directly, ligands that perform well across the three metals, metal-free controls showing several mechanisms including an aryne pathway, and common task assignments for community benchmarking. Design per the run's notes (not verified; the paper was not read): 2 amines x 4 aryl halides under 33 catalysts, 164 ligands, 17 bases, several temperatures and solvents, in 1536-well plates, assay yields by UPLC-MS.
- Use case: a process or medicinal chemist picks the metal, ligand, base and solvent for a C-N coupling before running it (as for `buchwald_hartwig_yields`); fit direct for the condition choice, approximate for a new substrate given 8 substrate pairs. Regime: IID over conditions, or grouped by substrate pair (8 groups, few for a grouped split); the paper's task assignments should decide (SPLIT-5, SPLIT-19).
- Siblings and duplicates: `buchwald_hartwig_yields` (TBD -> Yes, 3,955 reactions of one Pd screen, Ahneman et al. 2018) names this record as better data; the other reaction-yield records of the run, `amide_coupling_hte_47k`, `pfizer_hte_39k`, `suzuki_miyaura_hte_yields`, `pfizer_hitea_reaction_yield`, `uspto_reaction_yields`, `ord_reaction_yields` (TBD -> 2nd Tier) and `chempile_reaction_and_generated_tasks` (No), hold other reactions or labs: distinct tasks (PROV-7); none carries this ORD dataset id. External collections: the Open Reaction Database.
- Better data: found as better data for `buchwald_hartwig_yields` (the awesome-chemistry-datasets list; the curator's Zotero collection, item 149); no further search this round.
- Papers and pages: the JACS paper and the preprint (text not read: ACS refused the fetch and the Research Square page rendered empty); the ORD deposit; cernakHTE.
- Metric: not found: the paper's task assignments may fix one, unread; the field ranks yield models by R2 or RMSE on held-out reactions (see `buchwald_hartwig_yields`), so the fallback `rmse` on the yield (MET-1, MET-5, MET-8); inputs none.
- Risks for /add-dataset: read the paper's task assignments and splits first (PROV-16; PROV-17, ask the curator for the PDF); few substrates, so models learn conditions, and a random split over a factorial design can reduce to recognising the grid cell (the Chuang and Keiser critique of the Doyle set; run the naive controls, TP-4, TP-10); the metal-free controls (a "Blank" metal in the code's app) are rows to keep or drop by the task; the ligand column has about 164 levels (categorical, with descriptors); the ORD parquet holds nested reaction records to flatten into components; the yield is an assay yield, not isolated; the year is 2025 if the preprint's Globus link shared the data, else 2026 (PROV-9).
- Priority: gap 0 (chemistry and regression are covered), use case + (condition choice, the source's framing), source + (JACS paper, ORD deposit), shape + (50,688 reactions, categorical factors), risk - (8 substrate pairs; the paper's tasks unread).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 149: "TabPFN Extensions for Interpretable Geotechnical Modelling".
- as published: 50,688 reactions: 2 amines x 4 aryl halides under 33 catalysts, 164 ligands, 17 bases, several temperatures, diglyme, DMSO and binary solvent mixtures, in 1536-well plates; assay yields by UPLC-MS; ...; target: assay yield of the C-N coupling; access: open.
- Why: measured, systematic, about 13 times the Ahneman set, three metals compared directly
- Adds: better data for the Buchwald-Hartwig yield task (buchwald_hartwig_yields). Risks: only 8 substrate pairs, so models learn conditions rather than substrates and a grouped split by substrate pair has 8 groups; very high-cardinality ligand column
