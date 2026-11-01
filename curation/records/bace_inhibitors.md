---
unique_name: bace_inhibitors
name: BACE-1 inhibitors (Subramanian et al. 2016)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
source_links:
- https://doi.org/10.1021/acs.jcim.6b00290
- https://doi.org/10.1039/C7SC02664A
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): the BACE-1 inhibitor set of Subramanian et al. 2016 as merged in MoleculeNet (1,513 compounds with pIC50 and a binary label), the same data as `bace1_inhibitors`, which holds the screening.
- Source: Subramanian, Ramsundar, Pande and Denny 2016, "Computational Modeling of beta-Secretase 1 (BACE-1) Inhibitors Using Ligand Based Approaches", J Chem Inf Model (doi 10.1021/acs.jcim.6b00290), merged in MoleculeNet (Wu et al. 2018, Chem Sci, doi 10.1039/C7SC02664A, Sec. 3.1.11: "The BACE dataset provides quantitative (IC50) and qualitative (binary label) binding results for a set of inhibitors of human beta-secretase 1 (BACE-1)"); this record's links are these two DOIs, and its Assessment describes the same table ("1,513 SMILES with pIC50 and a binary active label").
- Siblings and duplicates: `bace1_inhibitors` (`TBD -> Yes`, priority 3, ChemPile) ends at the same paper and the same MoleculeNet file (doi 10.1021/acs.jcim.6b00290; deepchem bace.csv, 1,513 rows); its screening already names the two records one dataset (PROV-4). Same source, same rows, no distinct task (PROV-4, PROV-6).
- Better data: from the curator's Zotero collection (item 52); no further search this round.
- For the curator: `bace1_inhibitors` keeps the dossier and the ChemPile tag; this record's provenance (Zotero item 52, "Automatic Auxiliary Task Selection and Adaptive Weighting Boost Molecular Property ...") can move there. Which of the two stays is the curator's call.
- Reject check (AI, 2026-10-31): stands. Both records end at Subramanian et al. 2016 (https://doi.org/10.1021/acs.jcim.6b00290) and MoleculeNet's bace.csv (1,513 rows with pIC50 and Class). This record's pIC50 target and the kept record's binary Class are one framing choice: Class is a threshold of pIC50, and bace1_inhibitors' Risks already say to pick one. That is a swapped target, not a distinct task. Carry the pIC50 regression framing and Zotero item 52 to bace1_inhibitors.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 52: "Automatic Auxiliary Task Selection and Adaptive Weighting Boost Molecular Property ...".
- as published: compounds: 1,513 SMILES with pIC50 and a binary active label; target: pIC50 against human beta-secretase 1 (or active at a threshold); access: open.
- Why: Real binding measurements, regression or classification; part of the item's benchmark.
- Adds: No record. Small and single-target, so a lower priority than the AstraZeneca and Tox21 sets.
