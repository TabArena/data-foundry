---
unique_name: zeosyn_zeolite_synthesis
name: 'ZeoSyn: zeolite hydrothermal synthesis routes and their product framework'
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Many class
original_source: Github
year: '? (2023)'
domain: chemistry & material science
problem_type: Multiclass Classification
source_links:
- https://github.com/eltonpan/zeosyn_dataset
- https://doi.org/10.1021/acscentsci.3c01615
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 23,961 zeolite synthesis routes extracted from the literature (gel composition, conditions, OSDA, and the product framework or a failed synthesis), from MIT and ITQ, ACS Central Science 2024, MIT licence; a real synthesis-outcome task in a field no accepted dataset covers, with a long-tail target to define and routes to group by paper.
- Source: Pan, Kwon, Jensen, Xie, Gómez-Bombarelli, Moliner, Román-Leshkov and Olivetti, "ZeoSyn: A Comprehensive Zeolite Synthesis Dataset Enabling Machine-Learning Rationalization of Hydrothermal Parameters", ACS Central Science 10(3):729-743, online 2024-03-06 (CC BY 4.0, by Crossref); the data in github.com/eltonpan/zeosyn_dataset (MIT; repository created 2023-09-15, data first committed 2023-09-26; whether the repository was public then is not known, so the year is open between 2023 and 2024, PROV-9). As published: `dataset/ZEOSYN.xlsx` (11.3 MB, not downloaded), `osda_descriptors.csv` (4.6 MB), `zeolite_descriptors.csv` (0.7 MB). README: "23,961 zeolite synthesis routes, 233 zeolite topologies and 921 organic structure-directing agents (OSDAs)", each with "Gel compositions (molar ratios between heteroatoms, mineralizing agents, and water)", "Reaction conditions (crystallization/aging temperature and time)", the OSDA as SMILES and the product as a 3-letter IZA code; the demo notebook's outputs show element ratio columns (Si, Al, P, Na, K, Li, ..., F, Ge, H2O, OH), `cryst_temp`, `cryst_time`, `precursors` (text), `osda1 smiles` (879 distinct) and the products `Code1`, `Code2`, `Code3` (co-products); the README's figure caption says the paper metadata of each route ships too.
- Use case: a synthesis chemist, before running a hydrothermal synthesis, predicts which framework (or none) a gel, an OSDA and the conditions give, to choose the routes worth running; the paper frames its classifier as a way to rationalise the parameters (SHAP), so the decision is ours and the fit approximate (routes reported in papers, mostly successes). Regime: grouped by source paper (routes of one paper are variations of one recipe) or temporal by publication year; the authors' notebook splits at random (`train_test_split(X, y, test_size=0.2, random_state = random_state)`), a claim to check (SPLIT-5).
- Siblings and duplicates: no other record holds ZeoSyn (grep by zeolite, ZeoSyn, hydrothermal). Nearest records: reaction-outcome sets (`amide_coupling_hte_47k` TBD -> Yes, `buchwald_hartwig_yields`, `pfizer_hte_39k`) and MOF records (`mofsimplify_mof_stability`, literature-mined labels, not screened yet; `core_mof_gas_uptake`, `No`, simulated). External collections: listed in blaiszik/awesome-matchem-datasets (a list, not a benchmark); the run's other Zotero batch proposed it under the same name.
- Better data: from the curator's Zotero collection (items 191 and 99, awesome-matchem-datasets); no further search this round.
- Papers and pages: the ACS Central Science paper (pubs.acs.org returned 403; text not read, PROV-17); the repository's README, `utils.py` and `demo.ipynb` (read), and the first 3 MB of `classifier.ipynb`: a random forest on `Code1`, where an empty `Code1` becomes `'Failed'` ("Empty 'Code1' element means amorphous/dense phases - replace with 'Failed'"), on 21,972 routes after the OSDA merge, with `cryst_time` (1,412 missing) and `cryst_temp` (554 missing) imputed by an IterativeImputer fit on all rows.
- Metric: the notebook prints the accuracy and the macro averages of `classification_report` (precision, recall, F1) side by side; the paper's evaluation section was not read; no unique original found (MET-5), so the fallback `log_loss` on the framework classes as defined. Inputs none (the paper's DOI as the group if the split is grouped).
- Risks for /add-dataset: the target: 233 frameworks with a long tail, co-products in `Code2` and `Code3`, and `'Failed'` for amorphous or dense phases; cut it to the frequent frameworks plus "Others" and "Failed" as the notebook's confusion matrices do, or to the pore size (`get_pore_type` in `utils.py`), a choice for the curator (USE-5); `zeolite_descriptors.csv` describes the product framework, so joining it as an input leaks the label (LEAK); `osda1 smiles` and `precursors` are strings (descriptors ship for the OSDAs); failed syntheses are under-reported in papers (a possible `Selection Bias`, USE-8); group by paper on the shipped DOI (SPLIT-24); the paper's text from a free copy for quotes (PROV-16).
- Priority: gap + (multiclass is thin; no synthesis-outcome dataset is accepted), use case 0 (the paper rationalises; the decision is ours), source + (a peer-reviewed data paper from MIT and ITQ, an open repository), shape + (23,961 routes; ratios, conditions, OSDA descriptors, papers and years), risk - (the target to define; a leaking descriptor join).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 191: "blaiszik/awesome-matchem-datasets"; the curator's Zotero collection, item 99: "blaiszik/awesome-matchem-datasets".
- as published: 23,961 synthesis routes from 3,096 articles, 233 frameworks, 921 OSDAs (README and awesome list). dataset/ZEOSYN.xlsx is 11.3 MB, with osda_descriptors.csv (4.6 MB) and zeolite_descriptors.csv (0.7 ...; target: The zeolite framework obtained (multi-class over IZA codes, likely cut to the frequent ones, to pore-size class, or to success vs amorphous); access: open.
- Why: Real synthesis outcomes from the literature, with a peer-reviewed data paper, an open licence and ready OSDA descriptors. | real experiments extracted from the literature, with the outcome including failures; an established materials-synthesis task
- Adds: Prediction of inorganic synthesis outcomes, a domain no record covers. Caveats: 233 classes with a long tail; literature extraction (publication bias, mixed-phase products); routes from one paper are near-duplicates, so group by paper. Also proposed by zotero_27 under the same name. | no materials-synthesis dataset ...
