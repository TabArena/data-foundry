---
unique_name: pampa_ncats
name: pampa_ncats
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
collections:
- ChemPile
original_source: GOV Website
year: '2020'
domain: chemistry & material science
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://pubchem.ncbi.nlm.nih.gov/bioassay/1508612
- https://doi.org/10.1177/24725552211017520
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/pampa_ncats ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/pampa_ncats ; original: https://tdcommons.ai/single_pred_tasks/adme/#pampa-permeability-ncats'
- https://arxiv.org/abs/2505.12534
- https://opendata.ncats.nih.gov/adme/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: NCATS's own PAMPA (pH 7.4) results for about 2,000 compounds, one lab and one protocol, deposited with the measured permeability; an early-ADME screen whose source names the actor, with SMILES-only inputs handled as in the QSAR siblings.
- Source: NCATS (NCGC), PubChem AID 1508612 "NCATS Parallel Artificial Membrane Permeability Assay (PAMPA) Profiling", deposited 2020-10-05 (PubChem dates API), PI Pranav Shah; the public part of the in-house set of Sun et al. 2017 (Bioorg Med Chem 25:1266, PMID 28082071, cited by the AID: "7488 compound entries or 5,435 structurally unique molecules measured by the same lab"). As published: 2,528 CIDs (2,530 SIDs) with "Observed PAMPA at pH 7.4 (x 10-6 cm/sec)", a phenotype ("Low" 0-10, "Moderate" 10-100, "High" > 100) and the PubChem outcome: "active" for moderate or high (1,740 SIDs), "inactive" for low (295), "inconclusive" for N/F, "not found due to ... insolubility, non-specific binding" (about 495, no value). TDC's PAMPA_NCATS (Siramshetty et al. 2021, SLAS Discov 26:1326) keeps the 2,035 active and inactive compounds as a binary label on the SMILES, plus 142 approved drugs as an external set; ChemNLP and ChemPile-LIFT copy TDC. The run's note that the deposition is larger (2,528 against 2,035) counts the inconclusive rows, which have no value: no extra labelled compounds.
- Use case: a medicinal chemist in lead optimisation decides which designs to synthesise and send to cell-based permeability tests; the AID's description: the model "provides medicinal chemists a useful in-silico tool to facilitate design and synthesis of novel compounds with optimal drug-like properties". Fit direct (only the structure is needed before the assay). Regime: IID likely, with a scaffold-grouped variant to weigh (compounds from many NCATS projects; the deposition has no assay dates, so no temporal split); precedents qsar_oral_toxicity (IID kept, scaffold variant listed) and apistox (temporal on publication year).
- Siblings and duplicates: no other PAMPA record (searched pampa, permeab, ncats, AID 1508612); the same absorption family: `caco2_permeability_merged` (Caco-2, unscreened), `human_intestinal_absorption_hou`, `b3db_blood_brain_barrier`. The other NCATS Tier I depositions are other tasks: AID 1508591 (rat liver microsome stability, https://pubchem.ncbi.nlm.nih.gov/bioassay/1508591, moved here from source_links, PROV-12), AIDs 1508603 and 1508604 (cytosol stability). External collections: TDC (ADME, PAMPA_NCATS), ChemPile (ChemPile-LIFT `pampa_ncats`, arXiv 2505.12534), ChemNLP.
- Better data: no new search; a candidate of the benchmark ChemPile, also listed by the awesome-chemistry-datasets list. The run's Zotero attribution (item 117, "Product Market Regulation, Business Churning and Productivity") does not concern this dataset.
- Papers and pages: Sun et al. 2017 (the model on the full in-house set; abstract, quoted in the AID: SVR "AUC-ROC of 0.90", SVC "AUC-ROC of 0.88"; full text not available on Europe PMC); Siramshetty et al. 2021 (paywalled, not read); TDC's page ("predict whether it is has high permeability (1) or low-to-moderate permeability (0)").
- Metric: `roc_auc`, the fallback (MET-5, MET-8): Sun et al. report AUC-ROC in the abstract, one headline rather than a criterion shown to be chosen (full text not read); TDC has no leaderboard for this task; no threshold or cost beyond the class cut. Inputs: none.
- Risks for /add-dataset: the label: PubChem's outcome counts moderate as permeable (85% positive, 1,740 of 2,035), while TDC's text says "high (1) or low-to-moderate (0)" and the run's note says 69% positive: settle the cut on the deposition's values (the 10 and 100 cuts are the source's), and weigh a regression on the log permeability (problem_type is a choice); SMILES only, so the structure ships as RDKit 2D descriptors from the shared helper, as for every SMILES dataset (apistox, Lennart 2026-10-14); repeated structures (2,530 SIDs for 2,528 CIDs); the pH 5 PAMPA that NCATS also runs is not in this deposition.
- Priority: gap 0 (chemistry, binary and IID are not thin), use case + (the source names medicinal chemists and the design decision), source + (NCATS deposition with the protocol, two papers), shape + (about 2,000 compounds, about 200 descriptors, scaffold structure), risk 0 (the class cut is to settle on the source's values; no leak seen).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the benchmark ChemPile (https://arxiv.org/abs/2505.12534); the curator's Zotero collection, item 117: "Data for: Product Market Regulation, Business Churning and Productivity: Evidence from ...".
- as published: 2,035 compounds in the NCATS set (TDC); a second set of 142 approved drugs is not in ChemPile-LIFT; in ChemPile-LIFT 42,714 text prompts over 1 config(s); target: PAMPA permeability (high vs low-to-moderate); access: open.
- Why: Classify whether a compound passes a parallel artificial membrane permeability assay, the cheap screen before cell assays | one lab, one protocol, measured; the public part of NCATS' in-house Tier I data
- Adds: | already proposed by the ChemPile-LIFT scouting (same name) from the TDC copy; the first deposition is larger (2,528 against 2,035), and one compound set carries three Tier I endpoints. Risks: small; 69% positive; SMILES-only features
- Notes: Siramshetty et al. 2021 (SLAS Discov 26:1326), NCATS. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record.
