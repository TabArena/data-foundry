---
unique_name: herg_central
name: herg_central_at_10uM, herg_central_at_1uM, herg_central_inhib
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
collections:
- ChemPile
original_source: Other
year: '2011'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1089/adt.2011.0425
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/<config> (configs: herg_central_at_10uM, herg_central_at_1uM, herg_central_inhib) ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/herg_central_inhib ; original: https://tdcommons.ai/single_pred_tasks/tox/#herg-central'
- https://arxiv.org/abs/2505.12534
- https://pubchem.ncbi.nlm.nih.gov/bioassay/1511
- https://doi.org/10.7910/DVN/21LKWG
- https://tdcommons.ai/single_pred_tasks/tox/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 306,893 compounds measured for hERG block in one screen under one protocol, by far the largest and the most consistent of the three hERG candidates; the open points are which deposition the file comes from and which of the three labels ships.
- Source: Du, Yu, Zou, Babcock, Long, Li, "hERGCentral: a large database to store, retrieve, and analyze compound-human Ether-à-go-go related gene channel interactions", Assay Drug Dev Technol 9(6):580 (2011), doi 10.1089/adt.2011.0425, from the Johns Hopkins Ion Channel Center's electrophysiology screening of a ~300,000-compound library. As published and as TDC serves it: "**Dataset Statistics:** 306,893 drugs" with three labels on one table - `hERG_at_1uM` and `hERG_at_10uM` (percent inhibition, regression) and `hERG_inhib` (binary, "equivalent to hERG_at_10uM < -50"), plus the SMILES (tdcommons.ai/single_pred_tasks/tox; ChemNLP `herg_central_inhib/meta.yaml`, num_points 306,893, "A compound counts as a blocker if its IC50 is below 10 µM").
- Use case: the screener or medicinal chemist triaging compounds for hERG liability early, the decision the source states ("reliable prediction of hERG liability in the early stages of drug design is quite important to reduce the risk of cardiotoxicity-related attritions in the later development stages", TDC tox page); fit direct for the triage, since the data is the screen itself; regime grouped on the Bemis-Murcko scaffold (SPLIT-31 as amended; TDC's split for hERG data).
- Siblings and duplicates: `herg_blockers_wang` (648) and `herg_karim` (13,445) are the same endpoint from literature compilations, screened in the same batch - different first publications, so no duplicate by provenance (PROV-4, PROV-7), but one hERG task is enough and this is the single-lab one. The three ChemPile configs (`herg_central_at_1uM`, `herg_central_at_10uM`, `herg_central_inhib`) are three labels of one table, so one record, not three (PROV-6). External collections: ChemPile-LIFT (arXiv 2505.12534), TDC (not part of the 22-dataset ADMET Benchmark Group).
- Better data: a candidate of the benchmark ChemPile (this run searched no further).
- Papers and pages: Du et al. 2011 (publisher blocked the fetch, abstract not read); the TDC tox page; the ChemNLP builder.
- Metric: none found at the source - Du et al. 2011 is a database paper that ranks no model, hERG_Central is not in the TDC ADMET Benchmark Group's 22 datasets (tdcommons.ai/benchmark/admet_group/overview), and the TDC tox page names no metric - so the fallback: `rmse` for the percent-inhibition framing, `roc_auc` for the binary one (MET-5, MET-8); inputs none.
- Risks for /add-dataset: `hERG_inhib` is a deterministic rule on `hERG_at_10uM`, so one framing ships and the other labels are dropped and never become features (SEL-5, LEAK); the two concentrations are two measurements of the same compound, so one may not be a feature for the other; single-concentration HTS readouts are noisy and the percent values are signed; blockers are a small minority, so the class balance drives the metric choice (MET-9); the deposition behind the file is not pinned - PubChem AID 1511, which this record links, is the "Primary cell-based high-throughput screening assay for identification of compounds that protect hERG from block by proarrhythmic agents" by the Johns Hopkins Ion Channel Center (a 305,722-compound thallium-flux protection screen, read through PubChem's PUG REST description), which is a different readout from percent block, so the right AID and TDC's derivation have to be traced (PROV-8, PROV-15); features are the SMILES only.
- Priority: gap 0 (chemistry & material science has 12 accepted, not thin), use case + (the screen's own go/no-go), source + (a published database, a named screening centre, a TDC release), shape + (306,893 compounds, the largest measured chemistry table recorded), risk 0 (the open points are a provenance trace and a framing choice, not a leak or an unclear target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the benchmark ChemPile (https://arxiv.org/abs/2505.12534); the curator's Zotero collection, item 106: "Critical Assessment of ML models for ADMET Prediction in TDC leaderboards"; the curator's Zotero collection, item 93: "A Comparative Study to Benchmark Cross-Project Defect Prediction Approaches".
- as published: 306,893 compounds, three labels (TDC hERG_Central); in ChemPile-LIFT 8,899,897 text prompts over 3 config(s); target: hERG_at_1uM and hERG_at_10uM (percent inhibition); hERG_inhib (1/0); access: open.
- Why: Predict hERG channel block from structure: percent inhibition at 1 uM and at 10 uM, and the binary IC50-under-10-uM call | measured in one lab under one protocol, very large, and a safety decision every drug project makes | Very large, real screen with a clear go/no-go use
- Adds: | no cardiac-safety task in the benchmark, and a scale (300k rows) rare among measured chemistry tables. Risks: single-concentration HTS noise; AID 1511 is titled as a screen for compounds that protect hERG from block, so which deposition carries the inhibition values and how TDC derives hERG_inhib must be checked ...
- Notes: Three configs of one source, the hERG Central patch-clamp screen of Du et al. 2011 (Assay Drug Dev Technol 9:580); the three labels are three targets on the same table, which is how TDC ships it. The largest hERG dataset of the three in ChemPile-LIFT. Features: SMILES string only, so a container keeps the string and ...
