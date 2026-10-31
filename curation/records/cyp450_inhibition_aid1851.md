---
unique_name: cyp450_inhibition_aid1851
name: cyp_p450_1a2_inhibition_veith_et_al, cyp_p450_2c19_inhibition_veith_et_al, cyp_p450_2c9_inhibition_veith_et_al, cyp_p450_2d6_inhibition_veith_et_al, ...
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
year: '2009'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1038/nbt.1581
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/<config> (configs: cyp_p450_1a2_inhibition_veith_et_al, cyp_p450_2c19_inhibition_veith_et_al, cyp_p450_2c9_inhibition_veith_et_al, cyp_p450_2d6_inhibition_veith_et_al, cyp_p450_3a4_inhibition_veith_et_al) ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/cyp_p450_1a2_inhibition_veith_et_al ; original: https://tdcommons.ai/single_pred_tasks/adme/#cyp-p450-1a2-inhibition-veith-et-al ; PubChem AID 1851'
- https://arxiv.org/abs/2505.12534
- https://pubchem.ncbi.nlm.nih.gov/bioassay/1851
- https://tdcommons.ai/single_pred_tasks/adme/
- https://doi.org/10.3390/ijms17060914
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: one laboratory's qHTS panel of about 17,000 compounds against five CYP isozymes, measured labels on a decision every drug project makes; the strongest candidate of this ChemPile batch.
- Source: Veith, Southall, Huang et al., "Comprehensive characterization of cytochrome P450 isozyme selectivity across chemical libraries", Nat Biotechnol 27:1050, 2009 (https://doi.org/10.1038/nbt.1581), deposited as PubChem AID 1851 (NCGC; last data change 14 Jul 2009): "We determined potency values for 17,143 compounds against recombinant CYP 1A2, 2C9, 2C19, 2D6, and 3A4 enzymes through an in vitro bioluminescent assay" (abstract). As published (PUG REST assay summary): 17,143 substances, 16,560 compounds, a concentration-response curve per compound and isozyme with an activity call and AC50, "Compounds with AC50 equal or less than 10 uM are considered active"; 11,971 substances are inconclusive. TDC's binarised cuts hold 12,092 to 13,130 compounds per isozyme (1A2 12,579; 2C19 12,665; 2C9 12,092; 2D6 13,130; 3A4 12,328), SMILES and one label.
- Use case: a medicinal chemist flags a compound's drug-drug-interaction liability before synthesis or before the in-vitro CYP panel; the paper's own aim for the data is "to provide a foundation for testing and improving current CYP activity prediction models" (Discussion). Fit direct for the screening decision (predicting this assay's call for an untested compound is what the screen does), approximate for clinical interaction risk: "this database will be less sensitive towards time dependent inhibitors and will miss mechanism-based inhibitors" (Discussion). Regime grouped on the Bemis-Murcko scaffold (SPLIT-31).
- Siblings and duplicates: `tdc_cyp3a4_veith` (TabBench-Bio, "12,300 x 2,048" ECFP4 bits) is the same screen reached through TDC, so both records end at AID 1851 and one of them is a `Duplicate` (PROV-4, PROV-5): for the main session to merge, this record being the one that names the first publication. `cyp_substrates_carbon_mangels` covers the same enzymes with a different question (substrate, not inhibitor): distinct (PROV-7). The other PubChem screens on record are `butkiewicz_pubchem_hts`, `tox21`, `herg_central` and `muv_maximum_unbiased_validation`. The five isozymes are five cuts of one deposit (PROV-6): one isozyme ships as the dataset, the rest stay siblings in the comments.
- Better data: a candidate of the benchmark ChemPile (five ChemPile-LIFT configs) and of the curator's Zotero collection (items 66, 106, 137); no new search in this run.
- Papers and pages: the Nature Biotechnology paper (PMC2783980); PubChem AID 1851 (https://pubchem.ncbi.nlm.nih.gov/bioassay/1851); TDC's ADME page and ADMET leaderboard; the Milano group's curated 3A4/2C9 files (Nembri et al. 2016, https://doi.org/10.3390/ijms17060914), a later version of the same screen, not a source (PROV-8).
- Metric: the data's own publication declares none (it builds no model: "Many computational strategies have been advanced towards predictive CYP isozyme activity models", Discussion). TDC's ADMET leaderboard scores CYP2C9, CYP2D6 and CYP3A4 inhibition by AUPRC, its stated reason being that "AUPRC is used when the number of positive samples are much smaller than negative samples" (ADMET group overview) - the imbalance argument MET-9 rejects, and the decision does not act only on the top of the ranking, so the fallback `roc_auc` (MET-8), with TDC's choice named in the definition. Inputs none.
- Risks for /add-dataset: the release is SMILES-only, so the descriptors are ours (CLEAN-24) and salts, stereoisomers and exact copies must be checked (LEAK-16, LEAK-17); the binary call (AC50 cut, the inconclusive curve classes dropped) is TDC's processing of the deposit, so rebuild the label from AID 1851 if the call matters (USE-5, PROV-8, PROV-13); a strong class imbalance per isozyme; the AC50 column in the deposit would also support a potency regression.
- Priority: gap 0 (chemistry 12 accepted, binary and grouped not thin), use case + (a standard go/no-go in drug projects), source + (a single-laboratory screen with a paper and a public deposit), shape + (12,000+ compounds), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the benchmark ChemPile (https://arxiv.org/abs/2505.12534); the curator's Zotero collection, item 106: "Critical Assessment of ML models for ADMET Prediction in TDC leaderboards"; the curator's Zotero collection, item 137: "Data"; the curator's Zotero collection, item 66: "Benchmarking and Evaluation of AI Models in Biology: Outcomes and Recommendations from ...".
- as published: 1A2 12,579; 2C19 12,665; 2C9 12,092; 2D6 13,130; 3A4 12,328 compounds (TDC); in ChemPile-LIFT 1,255,880 text prompts over 5 config(s); target: inhibitor (1/0), one label per isoform; access: open.
- Why: Classify whether a compound inhibits a cytochrome P450 isoform, the drug-drug interaction screen in early ADME | measured by one centre with one qHTS protocol on a diverse library; a standard ADME decision in every project | Large single-lab screen, first-published on PubChem, the standard CYP benchmark | large, real ...
- Adds: | no drug-metabolism task in the benchmark; five related targets on the same compounds, so one is picked and the others stay siblings | ADMET, missing among the records (only toxicity and bioconcentration QSAR); one record with one isoform or five tasks | ADMET/CYP task (no record); first publication is PubChem AID ...
- Notes: Five configs of one source: Veith et al. 2009 (Nat Biotechnol 27:1050), a qHTS of about 17,000 MLSMR compounds against five isoforms, deposited as PubChem AID 1851 with full concentration-response curves, so the original also supports a potency regression. Features: SMILES string only, so a container keeps the string ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: both end at PubChem AID 1851 (`tdc_cyp3a4_veith`; PROV-4). The curator keeps one, or both as distinct tasks.
