---
unique_name: sarscov2_3clpro_diamond
name: sarscov2_3clpro_diamond
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
- https://www.diamond.ac.uk/covid-19/for-scientists/Main-protease-structure-and-XChem.html
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/sarscov2_3clpro_diamond ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/sarscov2_3clpro_diamond ; original: https://tdcommons.ai/single_pred_tasks/hts/#sars-cov-2-3cl-protease-diamond'
- https://arxiv.org/abs/2505.12534
- '# the first publication of the screen (71 active-site hits, 3 at the dimer interface)'
- https://doi.org/10.1038/s41467-020-18709-w
- '# the screen''s summary file named on the Diamond release page'
- https://www.diamond.ac.uk/dam/jcr:9fdc4297-15b6-47e2-8d53-befb0970bf7c/COVID19-summary-20200324.xlsx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a real crystallographic fragment screen turned into a hit/no-hit task by TDC, but only 879 fragments with roughly 70-80 hits, and SMILES as the single column.
- Source: the XChem fragment screen at Diamond Light Source against the SARS-CoV-2 main protease (3CL protease), spring 2020; the Diamond page the record links is the release page (403 here on 2026-10-31) and names the summary file `COVID19-summary-20200324.xlsx`. First publication of the screen: Douangamath et al., "Crystallographic and electrophilic fragment screening of the SARS-CoV-2 main protease", Nature Communications 11:5047, 7 Oct 2020 (https://doi.org/10.1038/s41467-020-18709-w; abstract read through the Crossref API): "Our crystallographic screen identified 71 hits that span the entire active site, as well as 3 hits at the dimer interface". The modelling cut comes through MIT AI Cures and TDC (`HTS(name="SARSCoV2_3CLPro_Diamond")`, the ChemNLP `transform.py` calls exactly that). As published in that cut: 879 rows (TDC page) or 880 (ChemNLP `meta.yaml`, `num_points: 880`), one identifier `SMILES` and one boolean target `activity_SARSCoV2_3CLPro`, "activity against the SARSCoV2 3CL protease (1) or not (0)"; licence CC BY 4.0 in the ChemNLP metadata. The positive share of the 879 rows was not checked (no download); the published screen is about 5-8% hits.
- Use case: a fragment-based drug-discovery chemist, before the next round of soaks or the next library, picks which fragments to test against the target (the framing AI Cures and TDC published it under); fit approximate, because the label is "observed bound in a crystal soak" under one protocol at one site, not potency; regime grouped on the Bemis-Murcko scaffold, because the rows are exact structures of a fragment library and a new candidate usually comes from a series that was not soaked (SPLIT-31 as amended 2026-10-26).
- Siblings and duplicates: no record held this data before (checked `curation/records/` for diamond, 3clpro, sarscov2, aicures, tdc). `sarscov2_invitro_touret` is the other COVID screen of the same ChemPile batch (a cell-based repurposing screen, a different assay and library: PROV-7, not a duplicate). Precedents for a SMILES-only molecule task: `apistox` (`Yes`; CC 2026-10-14: drop the SMILES as a feature, ship RDKit 2D descriptors from the shared helper), `qsar_tid_11` and `qsar_oral_toxicity` (`Yes`). Nearest `No`: `covid_19_drug_discovery_data` (Lennart, "clear scientific discovery task"), an undescribed Kaggle upload; this one has a named assay, a named library and a decision, so it is not that case, but the curator should confirm the line. Other virtual-screening candidates of this run: `butkiewicz_pubchem_hts`, `muv_maximum_unbiased_validation`, `tox21`. External collections: ChemPile-LIFT (`sarscov2_3clpro_diamond`), ChemNLP, TDC (HTS tasks), MIT AI Cures.
- Better data: a candidate of the benchmark ChemPile; no new search this run.
- Papers and pages: Douangamath et al. 2020 (above) is the data's paper; ChemNLP's `meta.yaml` cites instead Resnick et al. 2019 (JACS 141:8951, the electrophile-fragment screening method) and Xue et al. 2007 (JMB 366:965, Mpro production) — neither published these rows, so the citation has to be corrected (PROV-10). TDC HTS page: https://tdcommons.ai/single_pred_tasks/hts/#sars-cov-2-3cl-protease-diamond.
- Metric: none found. The TDC HTS page gives no metric (it lists random or scaffold splits only) and the SARS-CoV-2 sets are not in TDC's ADMET benchmark group, which is where TDC fixes metrics (https://tdcommons.ai/benchmark/admet_group/overview/); the Nat Commun paper defines a hit, not a model score. So the fallback for a binary task, `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: the positive count per fold (TP-5, TP-8: with about 74 hits a tenth-fold holds roughly 7); how TDC binarised the screen into `Y` and which 879 of the soaked fragments it kept, against the paper's own hit list (PROV-15); one column as published, so the features are whatever descriptor helper we run (apistox precedent); a scaffold split on fragments leaves very small groups (SPLIT-31).
- Priority: gap 0 (chemistry & material science, binary and grouped are not thin), use case + (a screening decision, published as a prediction task by AI Cures/TDC), source + (Nat Commun paper plus the Diamond release), shape - (879 rows, one column), risk - (a thin positive class and an undocumented binarisation).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 879 fragments (TDC; ChemNLP 880); in ChemPile-LIFT 17,600 text prompts over 1 config(s); target: 3CL protease hit (1/0).
- Why: Classify whether a fragment binds the SARS-CoV-2 main protease in the Diamond XChem crystallographic screen
- Notes: Diamond Light Source XChem fragment screen, 2020, distributed through MIT AI Cures; the cited method paper is Resnick et al. 2019 (doi 10.1021/jacs.9b02822). Very small. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record.
