---
unique_name: ncats_cytotoxicity_profiling
name: NCATS cytotoxic profiling of annotated and diverse chemical libraries (qHTS, HEK 293 and NIH 3T3)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2018'
domain: chemistry & material science
problem_type: Binary Classification
source_links:
- https://doi.org/10.1177/2472555219873068
- https://pubchem.ncbi.nlm.nih.gov/bioassay/1345083
- https://pubchem.ncbi.nlm.nih.gov/bioassay/1345082
- https://pubmed.ncbi.nlm.nih.gov/31498718/
- https://doi.org/10.1021/acs.jcim.4c01811
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: NCATS's cytotoxicity screen of 93,211 compounds in two normal cell lines, deposited in PubChem with dose-response calls and published with the decision it serves (avoid cytotoxic compounds early in screening); the label needs a rule for the 26,615 to 29,164 inconclusive compounds.
- Source: NCATS (NCGC), PubChem AID 1345083, "Cytotoxic Profiling in HEK 293 Cell Line of Diverse Libraries Using Quantitative High-Throughput Screening", and AID 1345082 (NIH 3T3), both deposited 2018-09-20 (PubChem dates API); paper: Lee, Austin, Gamma, ... Shen & Hall, "Cytotoxic Profiling of Annotated and Diverse Chemical Libraries Using Quantitative High-Throughput Screening", SLAS Discov 2019 (https://doi.org/10.1177/2472555219873068, PMC10791069). As published: per AID 93,211 compounds (93,776 substances); HEK 293: 6,153 active, 58,063 inactive, 29,164 inconclusive; NIH 3T3: 4,017 active, 62,722 inactive, 26,615 inconclusive (PubChem summaries); per compound the phenotype, curve class, AC50, efficacy, Hill fit and the response at each concentration; structures through the CID. The paper's annotated library (9,893 compounds, five cell lines) is another deposit, AID 1296008.
- Use case: the paper's: "allowing for the identification and avoidance of compounds with cytotoxicity during high-throughput screening campaigns" (abstract), and the AID's: "Prioritization of molecules with little or no cytotoxicity for a more in-depth downstream evaluation"; actor a screening scientist or medicinal chemist, moment before a compound is tested or followed up, decision drop or deprioritise it; fit direct (only the structure is needed). Regime IID, with a scaffold split as the question for new chemotypes (on a true scaffold id, SPLIT-24).
- Siblings and duplicates: `clock_protein_toxicity` (`Yes`; 171 molecules, Gul et al. 2021) and `clock_protein_period` (`No`, `Too Small`) are the records this was found for, from another source; other NCATS depositions in the records are other assays (`pampa_ncats`, `cyp450_inhibition_aid1851`), and `tox21` is another library and other assays. No record names AID 1345082 or 1345083 (searched). External collections: none among the records; Cyto-Safe (below) builds on both AIDs.
- Better data: found as better data for `clock_protein_toxicity` and `clock_protein_period`; no further search this run.
- Papers and pages: Lee et al. 2019 (read on PMC); Feitosa, Cabral, ... Andrade, "Cyto-Safe: A Machine Learning Tool for Early Identification of Cytotoxic Compounds in Drug Discovery", J Chem Inf Model 2024 (https://doi.org/10.1021/acs.jcim.4c01811), models built on "approximately 90,000 compounds, evaluated against two cell lines, 3T3 and HEK 293" (abstract; full text not read).
- Metric: the data's paper builds no model (hit rates, enrichment, Fisher's exact test and clustering, "Statistical analysis"); Cyto-Safe's metrics not read; so the fallback `roc_auc` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: the label: PubChem's active call (activity score 40-100 by curve class) against the paper's "high-quality" actives of the annotated library ("maximal response ≤ −50% and EC50 values less than 10 μM", Results), and the inconclusive third, which goes rather than counting as inactive (USE-5, USE-7); two cell lines are two targets on one compound set, so one dataset per line or one line (CLEAN-18); SMILES only, so the descriptors are ours (CLEAN-24), with salts and repeated substances to merge (93,776 substances for 93,211 CIDs; LEAK-16, LEAK-17); about 9.6% actives of the conclusive HEK 293 calls (6,153 of 64,216) and 6.0% for NIH 3T3 (4,017 of 66,739); the AID protocol says "48 or 72 hr" incubation, the paper 48 h.
- Priority: gap 0 (chemistry & material science, binary, IID not thin), use case + (the paper names the triage decision), source + (an NCATS deposit with its protocol and a paper), shape + (about 64,000 conclusive compounds per line), risk 0 (the label rule follows the source's own calls): 4.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `clock_protein_period`, `clock_protein_toxicity`.
- as published: PubChem AID 1345083 (HEK 293): 93,211 compounds, 6,153 cytotoxic, 58,063 non-cytotoxic, 29,164 inconclusive; AID 1345082 (NIH 3T3): 93,211 compounds, 4,017 cytotoxic, 62,722 non-cytotoxic. Screened ...; target: Binary cytotoxicity of a small molecule in a human (HEK 293) or mouse (NIH 3T3) cell line, from a CellTiter-Glo viability titration (active / inactive, or ...; access: open.
- Why: Same task as clock_protein_toxicity: predict whether a small molecule is toxic to cultured human cells from its structure, with features of the same kind (descriptors/fingerprints computed from the structure, as the apistox and clock_protein_toxicity definitions already do with the shared RDKit helper). Structures ...
- Adds: 93,211 compounds against 171 in clock_protein_toxicity (56 toxic), two cell lines instead of one, a named and documented assay with a stated activity threshold instead of an unexplained toxic/non-toxic call, and 2019 data instead of 2021 descriptors over a 171-molecule in-house series. Would turn a Tiny Data, ...
