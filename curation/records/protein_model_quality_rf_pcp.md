---
unique_name: protein_model_quality_rf_pcp
name: RF-PCP (quality assessment of modeled protein structures, CASP and decoy sets)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '2015'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://sourceforge.net/projects/rf-pcp/files/
- https://doi.org/10.1142/S0219720015500055
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata and notes below were drafted by an AI assistant from the release files and the paper's abstract; a human must verify them before relying on them.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: predict the quality (RMSD, TM-score or GDT_TS) of a modelled protein structure without its native, from six physicochemical properties; the decoy file names give the target protein, so the split can be grouped by target.
- Source: Rana, Sharma, Bhattacharya, Shukla, "Quality assessment of modeled protein structure using physicochemical properties", J Bioinform Comput Biol 13(2):1550005, April 2015 (doi:10.1142/S0219720015500055), with the authors' release on SourceForge (project rf-pcp, RF-PCP-DataSet.zip, 5.3 MB, 2014-08-18, user psrana; no licence stated). The abstract (Crossref): "a total of 95,091 modeled structures of 4896 native targets", features "total surface area, euclidean distance (ED), total empirical energy, secondary structure penalty (SS), sequence length (SL), and pair number (PN)", targets RMSD, TM-score and GDT_TS, k-fold cross-validation over structures. As published (per the old note, not re-opened): a full file of ~100k rows and CASP5-9 / CASP10 files with PDB-ID, RMSD, TM, GDT and the six features.
- Use case: a structure-prediction group or a CASP assessor ranks the candidate models of a new target before its native structure is known; fit approximate (the paper says the method makes "the prediction faster and inexpensive" but names no actor or decision); regime grouped by target protein because a new target has none of its decoys in training (the leak that retired `physiochemical_protein`).
- Siblings and duplicates: `physiochemical_protein` (UCI 2013, the same group's earlier file, `No (Retired)` by Lennart on 2026-10-06 because no copy has target ids; the CC line names RF-PCP as a candidate to triage) and `physiochemical_protein_duplicate`; this release has other features and cannot be joined to the UCI rows, so it is a distinct dataset (PROV-7). External collections: none found.
- Papers and pages: the 2015 paper above; Pathak, Rana et al., Int J Data Mining and Bioinformatics (online 2015-11, RMSD <= 5 A with the same six properties) used the same features.
- Metric: the paper reports RMSE, correlation, R^2 and accuracy (within +-0.1) for each of the three targets, none ranked, so the fallback `rmse` on the chosen target (MET-5); inputs none.
- Risks for /add-dataset: which target to ship (GDT_TS or TM-score, the bounded scores QA methods predict, against RMSD of the UCI file); the rows mix CASP decoys with classic decoy sets and native structures (RMSD 0, not known at prediction time for a new target); Energy outliers up to 7e11; SL and PN near-constant within a target; six coarse features that structure-based deep QA models have since replaced (`Outdated` question, SEL-12 boundary).
- Priority: gap + (biology & life sciences and the grouped regime are thin), use case 0 (no actor named by the source), source +, shape +, risk - (target choice, natives, outdated features).

**What it is (AI, 2026-10-06).** The supplement of Rana, Sharma, Bhattacharya and Shukla (2015), "Quality assessment of modeled protein structure using physicochemical properties" (J Bioinform Comput Biol 13(2):1550005): predict the RMSD, TM-score and GDT_TS of a modeled protein structure, without its native structure, from six physicochemical properties (total surface area, Euclidean distance, total empirical energy, secondary structure penalty, sequence length, pair number). The abstract reports "95,091 modeled structures of 4896 native targets" and k-fold cross-validation over the structures (random forest best, R^2 0.92 for RMSD). The files are on SourceForge (project rf-pcp, registered 2014-08-18, RF-PCP-DataSet.zip, 5.3 MB): RF-PCP-Full-dataset.csv (99,987 rows), RF-PCP-Training-Testing-CASP-5-9.csv (92,597) and RF-PCP-Validation-CASP-10.csv (5,119), with the columns PDB-ID, RMSD, TM, GDT, Area, ED, Energy, SS, SL and PN.

**Why a candidate.** It can replace physiochemical_protein (retired 2026-10-06): the same group's UCI file has no target ids, so its decoys could not be split by protein. Here the PDB-ID names each decoy file, so the target is known: CASP5-10 decoys of 342 targets (34,288 rows, a median of 101 per target; e.g. `CASP10_T0719_PconsD_TS5.pdb`), classic decoy sets named by the native's PDB code (ROSETTA 17,077, lattice 14,329, fisa 8,334, rosetta62 7,189, John2002 5,923, 4state 4,160, lmds 3,863 rows) and 4,478 native structures. The use case, judging the models of a new target, needs grouped splits by target (the native protein; one native can occur in several decoy sets); the source's CASP10 file is a natural test on a new CASP round.

**Open questions for triage.**
- Licence: none stated on the SourceForge page.
- Target: GDT_TS or TM-score (the bounded scores that quality-assessment methods predict) or RMSD (the UCI version's target).
- Rows: CASP decoys only, or all decoy sets; the native structures are trivially perfect (RMSD 0), and in a new-target setting the native is not known.
- Features: six only; Energy reaches 7e11 (outliers to check); SL and PN are constant within most CASP targets (80% and 71%), so they identify the protein, which is fine under a grouped split.
- One PDB-ID occurs twice in the full file.

## Reference

Rana PS, Sharma H, Bhattacharya M, Shukla A. Quality assessment of modeled protein structure using physicochemical properties. J Bioinform Comput Biol 13(2):1550005 (2015). doi:10.1142/S0219720015500055
