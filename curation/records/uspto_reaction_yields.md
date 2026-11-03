---
unique_name: uspto_reaction_yields
name: uspto_yield
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
collections:
- ChemPile
original_source: Other
year: '2017'
domain: chemistry & material science
problem_type: Regression
source_links:
- https://doi.org/10.6084/m9.figshare.5104873
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/uspto_yield ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/uspto_yield ; original: https://figshare.com/articles/dataset/Chemical_reactions_from_US_patents_1976-Sep2016_/5104873'
- https://arxiv.org/abs/2505.12534
- https://www.repository.cam.ac.uk/handle/1810/244727
- https://open-reaction-database.org/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a large, CC0, traceable reaction corpus with a real target (the reported yield), but the yield is text-mined from patent prose, the release duplicates reactions by design, and the ChemPile cut is a small and oddly built slice of it.
- Source: Daniel Lowe, "Chemical reactions from US patents (1976-Sep2016)", figshare, published 2017-06-13, licence CC0 (https://doi.org/10.6084/m9.figshare.5104873, read through the figshare API): reactions text-mined from US patents, released as CML and as reaction SMILES, in four archives (grants 1976-Sep2016 and applications 2001-Sep2016, about 1.5 GB of CML). The extraction method is Lowe's Cambridge thesis (https://www.repository.cam.ac.uk/handle/1810/244727) with LeadMine for entity recognition. The SMILES files carry "tab delimited columns for: PatentNumber, ParagraphNum, Year, TextMinedYield, CalculatedYield", so the target, a document id and a year all ship. The ChemPile/ChemNLP cut is much smaller: 36,564 one-product reactions with a yield (`uspto_yield`, licence CC0, identifiers `RXNSMILES`, `educt_string`, `product_string`, target `yield` in %), built from `kjappelbaum/chemnlp-uspto` by keeping `WithinTolerance == True` and `MeanYield`.
- Use case: a process or medicinal chemist, planning a synthesis, estimates the yield of a proposed reaction before running it (and so which route to try); fit approximate, because a patent reports the yield of one run under conditions that the reaction SMILES does not carry; regime not settled — temporal is natural and available (the Year column, 1976-2016, matches "train on what is published, predict the next chemistry"), with grouping by patent document or by product scaffold as the alternative, since many reactions come from one paragraph or one patent family; the field is left empty on purpose.
- Siblings and duplicates: `chempile_reaction_and_generated_tasks` holds the same Lowe source under its `uspto` config as a product-prediction (generation) task — one source, a different task, so PROV-7 rather than a duplicate, but the two records must stay apart. `ord_reaction_yields` (Open Reaction Database) is a different publisher whose database has imported USPTO-derived reactions, so check the overlap before both enter (PROV-4, PROV-6); its ChemNLP yield configs are 28 and 30 rows. High-throughput-experimentation yield records are other sources and other tasks: `buchwald_hartwig_yields`, `suzuki_miyaura_hte_yields`, `amide_coupling_hte_47k`, `pfizer_hitea_reaction_yield`, `catechol_solvent_selection_yields`. External collections: ChemPile-LIFT (`uspto_yield`), ChemNLP, the awesome-chemistry-datasets list; the Open Reaction Database carries the same corpus.
- Better data: a candidate of the benchmark ChemPile (also the awesome-chemistry-datasets list and the curator's Zotero collection); no new search this run.
- Papers and pages: Lowe's thesis (the extraction method) and the figshare record (the data); the figshare page is the citable reference (PROV-10); https://open-reaction-database.org/ for the overlapping corpus.
- Metric: none found. The figshare description defines no task and no score, and the ChemNLP metadata declares no metric; the yield-prediction literature reports R², RMSE and MAE side by side, which is no unique original (MET-5). So the regression fallback `rmse` (MET-8); inputs none. Yields are bounded at 0-100%, which is a modelling-scale question (MET-3), not a metric one.
- Risks for /add-dataset: the source's own warning on duplicates — "Duplicate reactions are frequent due to the same or highly similar text occurring in multiple patents, this is especially true when combining the applications and grant datasets, many reactions from applications will later appear in patent grants" — so near-duplicate rows can sit on both sides of a split (LEAK, PROV-6); the same page warns that "the atom-maps are wrong in many cases and hence should not be entirely relied on"; yields are as reported in the patent, noisy and biased to successful runs, and the literature reports patent-yield prediction as hard (Schwaller et al. 2021, not re-checked here) — a task probe on a sample should come before any build (TP-2, TP-3); `TextMinedYield` against `CalculatedYield` have to be reconciled (the ChemNLP cut used a `MeanYield` with a tolerance flag); the ChemNLP builder reads the same `..._test_prompts.json` file for train, test and valid, so that cut is not a source to build from (PROV-15); the features are reaction SMILES, so a container needs an explicit component/condition split, as `buchwald_hartwig_yields` has; the release is 7z archives of CML per year, so the table has to be built (`Needs extensive data wrangling`).
- Priority: gap 0 (chemistry & material science, regression are not thin), use case 0 (the source publishes a corpus, not a decision), source + (a named author, a thesis, a CC0 figshare release), shape + (36,564 rows in the small cut, far more in the full release), risk - (text-mined noisy yields, frequent duplicates, an overlap with the ORD record).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the benchmark ChemPile (https://arxiv.org/abs/2505.12534); the curator's Zotero collection, item 147: "TabPFN-2.5: Advancing the State of the Art in Tabular Foundation Models".
- as published: 36,564 reactions with a yield (ChemNLP cut of Lowe's patent set); in ChemPile-LIFT 182,820 text prompts over 1 config(s); target: yield (%); access: open.
- Why: Predict the reported yield of a reaction mined from a US patent | real, large, CC0, the classic open reaction source
- Adds: | already proposed by the ChemPile-LIFT scouting (same name). Risks: text-mined, with frequent duplicates between grants and applications; yields biased to successful runs and noisy, reported as hardly predictable in the yield-prediction literature (Schwaller et al. 2021; not re-checked); reaction SMILES needs a ...
- Notes: Daniel Lowe's text-mined US patent reactions, 1976-2016 (his 2012 thesis, figshare release, CC0). Yields are as reported in patents, which is noisy and biased to successful runs; the features are reaction SMILES, so a tabular container needs a condition/component split like the Buchwald one. No record.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: possible row overlap, since ORD imported USPTO-derived reactions; check before both enter (`ord_reaction_yields`; PROV-6). The curator keeps one, or both as distinct tasks.
