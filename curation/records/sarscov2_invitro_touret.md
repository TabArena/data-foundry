---
unique_name: sarscov2_invitro_touret
name: sarscov2_vitro_touret
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Tiny Data
- Non-IID (Grouped)
collections:
- ChemPile
original_source: Other
year: '2020'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1038/s41598-020-70143-6
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/sarscov2_vitro_touret ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/sarscov2_vitro_touret ; original: https://tdcommons.ai/single_pred_tasks/hts/#sars-cov-2-in-vitro-touret-et-al'
- https://arxiv.org/abs/2505.12534
- '# open-access copy of the paper; the full screen (every compound) is its supplementary material'
- https://pmc.ncbi.nlm.nih.gov/articles/PMC7403393/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a documented one-plate repurposing screen of 1,480 approved drugs with about 90 hits, published as a screening result and turned into a prediction task by AI Cures and TDC; SMILES is the only column.
- Source: Touret, Gilles, Barral, Nougairede, van Helden, Decroly, de Lamballerie, Coutard, "In vitro screening of a FDA approved chemical library reveals potential inhibitors of SARS-CoV-2 replication", Scientific Reports 10:13093, Aug 2020 (https://doi.org/10.1038/s41598-020-70143-6, read open access at https://pmc.ncbi.nlm.nih.gov/articles/PMC7403393/): 1,520 off-patent, mostly FDA-approved molecules of the Prestwick Chemical Library, each at 10 µM, in a VeroE6 infected-cell assay (MOI 0.002, CellTiter-Blue read three days after infection), each plate normalised to an arbidol control to give an Inhibition Index; a compound counts as a hit at Inhibition Index 1 or more, which gave 90 compounds (5.85%); the authors state that the raw data for every compound is in the supplementary material, so a reader can set another cutoff. As published through TDC/AI Cures (`HTS(name="SARSCoV2_Vitro_Touret")`): 1,480 rows (TDC page) or 1,484 (ChemNLP `meta.yaml`), one identifier `SMILES` and the boolean `activity_SARSCoV2`, "whether it is active against SARSCoV2 (1) or not (0)"; licence CC BY 4.0 in the ChemNLP metadata.
- Use case: a repurposing screener picks which approved drugs go into the next (cell or animal) test — the paper's own framing, "reveals potential inhibitors"; fit approximate, because the label is one cell line at one concentration in one laboratory, not clinical activity; regime grouped on the Bemis-Murcko scaffold, because the rows are exact structures and a candidate drug usually comes from a chemical series that was not screened (SPLIT-31 as amended 2026-10-26).
- Siblings and duplicates: no earlier record (checked for touret, sarscov2, prestwick, aicures); the repo's COVID records are clinical (`curial_covid_ed_triage`, `sirio_libanes_covid_icu`, `covid_trials`). `sarscov2_3clpro_diamond` is the other COVID screen of this ChemPile batch: another assay, another library, so PROV-7 rather than a duplicate. SMILES-only precedents that shipped: `apistox` (`Yes`), `qsar_tid_11`, `qsar_oral_toxicity`. Nearest `No`: `covid_19_drug_discovery_data` ("clear scientific discovery task", an undescribed Kaggle upload) — this one names the library, the assay and the hit rule, so the facts differ; the curator should confirm. External collections: ChemPile-LIFT (`sarscov2_vitro_touret`), ChemNLP, TDC (HTS), MIT AI Cures.
- Better data: a candidate of the benchmark ChemPile; no new search this run.
- Papers and pages: the Scientific Reports paper above (data in its supplementary); TDC page https://tdcommons.ai/single_pred_tasks/hts/#sars-cov-2-in-vitro-touret-et-al.
- Metric: none found. The paper defines a hit, not a model score, and states no prediction task ("the paper does not define a machine-learning or predictive modeling task"); the TDC HTS page names no metric (random or scaffold split only) and these sets are outside TDC's ADMET benchmark group, where TDC fixes metrics (https://tdcommons.ai/benchmark/admet_group/overview/). So the binary fallback `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: the positive count per fold (about 88 hits, so roughly 9 in a tenth-fold; TP-5, TP-8); which cutoff TDC used, since the paper gives two hit lists (90 by Inhibition Index, 56 by the statistical filter, 14 in both) and the TDC cut has 1,480 of the 1,520 screened compounds (PROV-15) — the paper's supplementary table settles both; one column as published, so the features come from the shared RDKit descriptor helper (`apistox` precedent); small groups under a scaffold split.
- Priority: gap 0 (chemistry & material science, binary and grouped are not thin), use case + (the screener's decision, named by the paper), source + (an open-access paper with the raw screen in its supplement), shape - (1,480 rows, one column), risk - (a thin positive class and an unverified binarisation).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 1,480 approved drugs (Prestwick library; ChemNLP 1,484); in ChemPile-LIFT 29,680 text prompts over 1 config(s); target: SARS-CoV-2 activity (1/0).
- Why: Classify whether an approved drug inhibits SARS-CoV-2 replication in a cell-based assay (repurposing screen)
- Notes: Touret et al. 2020 (Sci Rep 10:13093), through MIT AI Cures. Small, one-off repurposing screen. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record (covid records in the repo are clinical, not screening).
