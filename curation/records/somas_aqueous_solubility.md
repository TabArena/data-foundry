---
unique_name: somas_aqueous_solubility
name: 'SOMAS: Solubility of Organic Molecules in Aqueous Solution'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2022'
domain: chemistry & material science
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.6084/m9.figshare.14552697
- https://doi.org/10.1038/s41597-022-01814-4
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, papers and a preview of the files, NOT from a full inspection of the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: PNNL's SOMAS (Sci Data 2022, CC BY 4.0), 11,696 neutral organic molecules with an experimental aqueous solubility in mg/L at a stated temperature, merged from six sources with conflicts checked against the original references, plus DFT and 2D descriptors; a larger aqueous-solubility set than AqSolDB from partly the same literature, so the curator picks one, and part of its values came through EPI Suite.
- Source: Gao, Andersen, Sepulveda, Panapitiya, Hollas, Saldanha, Murugesan and Wang, "SOMAS: a platform for data-driven material discovery in redox flow battery development", Sci Data 9:740 (2022-12-01, doi 10.1038/s41597-022-01814-4; read on PMC9715657). Six sources (Methods): GDB-13 and GDB-17 molecules "checked" with EPA EPI Suite and PubChem (1,068), ChEMBL25 checked with EPI Suite (2,122), NIST SRD106 (149), OCHEM (2,791), eChemPortal (1,743) and Cui et al. (3,823); "The unit of solubility in our database is mg/L"; with several temperatures "only the solubility value which is the closest to room temperature is selected"; values differing by more than 50% were checked "manually" against "the original references". Figshare (doi 10.6084/m9.figshare.14552697): v1 2022-10-31 (no files), v2 and v3 November 2022 (`dataset.csv`, `xyzfile.tar.gz`), v4 2024-03-04 adds `datasetv2.csv` and `xyzfilev2.tar.gz` without a stated reason. `datasetv2.csv` (head previewed): 26 columns, Name, SMILES, Molar Mass, CAS Number, `Experimental Solubility in Water`, `Temperature` (K, 288-298 in the preview), `Experiment Reference`, `Datagroup` (G2 rows cite Yalkowsky and Horvath, G3 a J Fluorine Chem paper, G4 OChem, G5 ECHA dossiers: apparently one group per source), `Solvation Energy` (COSMO, DFT), dipole, volume, surface area, three quadrupole components, HOMO, LUMO, gap, InChIKey, six RDKit/Mordred descriptors and `Isomer`.
- Use case: the paper's: aqueous organic redox flow batteries need molecules far more soluble than drugs ("much larger (>=0.5 M) than that of the drug molecules (<0.1 M)"), and SOMAS is "a platform for data-driven material discovery" there; a chemist screening candidate electrolyte molecules estimates the solubility before synthesis; fit approximate, since the rows are organics measured for other purposes, not battery candidates. Regime grouped on the Bemis-Murcko scaffold (SPLIT-31), as for `aqsoldb`; the paper trains no model and gives no split.
- Siblings and duplicates: `aqsoldb` (`TBD -> Yes`, 3; 9,982 compounds merged from nine datasets including eChemPortal, salts and inorganics included): another compilation, not a duplicate (PROV-4), with overlapping compounds and sources; the curator picks one of the two, or ships both with the overlap removed. `tdc_aqsoldb` (`No`, `Duplicate` of `aqsoldb`); `solprop_solvation_free_energy` (its logSaq part is aqueous solubility too); `bigsoldb_2` and `drug_solubility_binary_solvent_mixtures` (organic solvents, PROV-7). External collections: awesome-chemistry-datasets.
- Better data: from the awesome-chemistry-datasets list and the curator's Zotero collection (item 92); no further search this round.
- Papers and pages: Gao et al. 2022 (the data); a 2025 University of Washington thesis ("Solvation Meta Predictor") trains ensembles on it.
- Metric: none found (the paper trains no model; its only error figure is an RMSE of 1.82 of its COSMO-SMD solvation energies against experiment on 308 molecules, Technical Validation), so the fallback `rmse`, on log solubility (the target spans orders of magnitude; ship it as log and score on the scale the add stage fixes, MET-3); inputs none.
- Risks for /add-dataset: whether the EPI Suite groups (1 and 2) are experimental values (PHYSPROP) or EPI Suite estimates is not stated; the G2 rows previewed cite experimental references, G1 was not seen (PROV-3, a check on the data); temperatures range over about 10-30 C and are missing for part of source 6 ("We recommend users to consider the temperature effect", Usage Notes): keep the temperature as a feature or filter; `dataset.csv` against `datasetv2.csv` (PROV-6: which version, and why it changed); `Datagroup` and `Experiment Reference` describe the label's origin and are no features (LEAK); `Solvation Energy` is computed from the structure (CLEAN-24), not a label; stereoisomers that share a 2D structure (`Isomer`, LEAK-17).
- Priority: gap 0 (chemistry & material science and regression are not thin), use case 0 (the battery use is named but the rows are not battery candidates), source + (a data paper with documented sources and a CC BY release), shape + (11,696 molecules, 20 descriptors of several kinds), risk - (the EPI Suite groups and mixed temperatures make the target partly unclear).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 92: "gabriead/kilterboard_grade_predictor".
- as published: 11,696 neutral organic molecules (paper) with experimental aqueous solubility, measurement temperature, literature reference and data group, plus 8 DFT descriptors and 2D descriptors; datasetv2.csv ...; target: experimental solubility in water at the stated temperature (unit to verify; methane 22, trifluoromethane 4090, so apparently mg/L); access: open.
- Why: measured target, neutral organics only, conflicting literature values checked by hand against the original references (paper); the DFT descriptors are computed features, not labels
- Adds: about 1.7k more compounds than AqSolDB and about twice as many highly soluble ones (paper); a temperature per value. Shares sources with AqSolDB (eChemPortal/ECHA, Yalkowsky): the curator picks one of the two
