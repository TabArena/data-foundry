---
unique_name: ord_reaction_yields
name: ord_rxn_smiles_yield_pred, ord_steps_yield
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Too Small
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
collections:
- ChemPile
domain: chemistry & material science
problem_type: Regression
source_links:
- https://doi.org/10.1021/jacs.1c09820
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/<config> (configs: ord_rxn_smiles_yield_pred, ord_steps_yield) ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/ord_rxn_smiles_yield_pred ; original: https://github.com/open-reaction-database/ord-data'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: the ChemPile cut holds 28 and 30 reactions with a yield, far too few; the Open Reaction Database hosts many datasets first published elsewhere, several of them records already, so a task from it would be one of those datasets, not this cut.
- Source: Kearnes, Maser, Wleklinski, Kast, Doyle, Dreher, Hawkins, Jensen and Coley, "The Open Reaction Database", J. Am. Chem. Soc. 143:18820, online 2021-11-02 (https://doi.org/10.1021/jacs.1c09820), abstract: "an open-access schema and infrastructure for structuring and sharing organic reaction data, including a centralized data repository"; ord-data (https://github.com/open-reaction-database/ord-data): "Each file holds one dataset", CC BY-SA 4.0, the USPTO grants split into "41 datasets, 1976–2016". As cut by ChemNLP from a compilation (Hugging Face kjappelbaum/chemnlp-ord, `ord_data_compiled.json`): `ord_rxn_smiles_yield_pred`, a reaction SMILES and the yield (%), `num_points: 28`; `ord_steps_yield`, a written action sequence and the yield, `num_points: 30` (meta.yaml of each builder).
- Use case: a chemist predicts the yield of a planned reaction to choose its conditions (ChemNLP's template: "I want to run a reaction with ... What is the yield I can expect?"); fit approximate, and in practice within one reaction class. Regime: set by the ORD dataset chosen (by substrate, grouped, or IID within an HTE plate).
- Siblings and duplicates: ORD datasets with their own records: `uspto_reaction_yields` (Lowe's patent reactions), `buchwald_hartwig_yields` (ORD dataset 46ff9a32...), `suzuki_miyaura_hte_yields`, `pfizer_hte_39k`, `amide_coupling_hte_47k`, `cn_coupling_hte_50k` (each links an ORD dataset file); `chempile_reaction_and_generated_tasks` (the other ORD configs of ChemPile, product and procedure generation). Which ORD datasets the 28 and 30 rows come from is not stated, so no duplicate is confirmed (PROV-5). External collections: ChemPile (configs `ord_rxn_smiles_yield_pred`, `ord_steps_yield`).
- Better data: a candidate of the benchmark ChemPile; no further search for this run's finds.
- Papers and pages: Kearnes et al. 2021 (abstract read); the ORD overview (https://docs.open-reaction-database.org/en/latest/overview.html), its purpose: "support machine learning and related efforts in reaction prediction, chemical synthesis planning, and experiment design"; ChemPile, arXiv 2505.12534.
- Metric: none found (the ChemNLP meta.yaml names no benchmark, the ORD paper's abstract and overview define no task), so the fallback `rmse` on the yield (MET-1).
- Risks for /add-dataset: 28 and 30 rows (TP-5); the inputs are a reaction SMILES string and a free-text procedure (SEL-12), so a table needs the reaction split into its components, as `buchwald_hartwig_yields` plans; reactions of many classes mixed; a later record names one ORD dataset that no record holds yet, under its own first publication (PROV-8).
- Priority: gap 0 (chemistry has 12 accepted datasets, regression is not thin), use case 0 (fit approximate), source + (a JACS paper and a maintained repository), shape 0 (28 and 30 rows), risk - (a tiny cut with text inputs, overlapping recorded ORD datasets).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 28 and 30 reactions with yields in the ChemNLP cut; in ChemPile-LIFT 377 text prompts over 2 config(s); target: yield (%).
- Why: Predict the yield of a reaction recorded in the Open Reaction Database
- Notes: Open Reaction Database (Kearnes et al. 2021, JACS 143:18820). Two configs of the same source; the yield subsets are tiny here (28 and 30 rows), far too small for a record, though ORD itself keeps growing and would be worth a later look as a reaction-condition table.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: possible row overlap, since ORD imported USPTO-derived reactions; check before both enter (`uspto_reaction_yields`; PROV-6). The curator keeps one, or both as distinct tasks.
