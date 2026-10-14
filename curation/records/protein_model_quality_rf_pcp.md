---
unique_name: protein_model_quality_rf_pcp
name: RF-PCP (quality assessment of modeled protein structures, CASP and decoy sets)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
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
