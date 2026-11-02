---
unique_name: bigsoldb_2
name: 'MixtureSolDB: solubility of organic compounds in binary solvent mixtures at various temperatures'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.18660057
- https://doi.org/10.1038/s41597-026-07047-z
- https://doi.org/10.5281/zenodo.15094979
- https://doi.org/10.1038/s41597-025-05559-8
- https://doi.org/10.5281/zenodo.6809668
- https://doi.org/10.5281/zenodo.6984601
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: MixtureSolDB (2026), 175,166 literature solubility values of 810 organic solutes in 750 binary solvent mixtures at 252-383 K, a large open regression for choosing a solvent mixture; the record also carries BigSolDB 2.0 (single solvents, 2025), a separate dataset of the same group that needs its own record.
- Source: Malikov, Krasnov, Kiseleva, Meshcheriakova, Kuznetsov, Elistratov, Vasiyarov, Tatarin and Bezzubov (Kurnakov Institute of General and Inorganic Chemistry RAS; Lomonosov Moscow State University), "Dataset of solubility values for organic compounds in binary mixtures of solvents at various temperatures", Scientific Data 2026 (doi 10.1038/s41597-026-07047-z, online 2026-03-20); Zenodo 10.5281/zenodo.18660057 (v3, CC BY 4.0). As published: MixtureSolDB.csv (41 MB), 175,166 rows x 20 columns (record id, solute and solvent SMILES, temperature, solubility as mole fraction and in g/100 g with their logs, solvent names, fractions and fraction type, compound name, CAS, PubChem CID, FDA flag, source DOI, a pure-solvent endpoint flag), plus solvent boiling points and an abbreviation legend; 3,001 solute-mixture systems from 1,115 articles, literature searched to October 2025 (Methods). BigSolDB 2.0 (Krasnov et al., Scientific Data 2025, doi 10.1038/s41597-025-05559-8; Zenodo 15094979, 2025-03-27): 103,944 values, 1,448 solutes, 213 single solvents, 243-425 K, 1,595 articles; BigSolDB 1.0 (Zenodo 6984601, 2022, 54,273 values, 830 solutes, 138 solvents) is its earlier version (PROV-6).
- Use case: a process or formulation chemist picks a solvent mixture and a temperature (crystallization, reaction medium, formulation) for a compound before measuring its solubility; the descriptor names the applications (mixtures give "a more diverse set of reaction media and crystallization conditions", measurement is "time- and labor-consuming", Background) but no actor; fit approximate (literature values from many labs); regime grouped by solute, on the Bemis-Murcko scaffold (SPLIT-31), since many temperatures and fractions per solute-mixture system would otherwise sit on both sides.
- Siblings and duplicates: `drug_solubility_binary_solvent_mixtures` (the CheMixHub copy of Bao et al. 2024, 27,166 values, 169 molecules) is the same task from an earlier compilation, which the descriptor's comparison table lists ("BaoDB (2024)": 28,098 values, 125 solutes; "MixSolDB (2025)": 34,734): another source, so not a duplicate (PROV-4), but the rows overlap through the same articles, and MixtureSolDB is larger and newer, so the curator will likely want one of the two; `aqsoldb`, `tdc_aqsoldb` and `somas_aqueous_solubility` are aqueous solubility; `solprop_solvation_free_energy` overlaps BigSolDB in its solid solubilities. This record mixes two datasets: its `unique_name` names BigSolDB 2.0, its `name` and Assessment MixtureSolDB; single-solvent and mixture solubility are distinct tasks (PROV-7), so one record each. External collections: none found.
- Better data: from the curator's Zotero collection (items 50, 72, 99), the awesome-chemistry-datasets list and the dead-link check; no further search this round.
- Papers and pages: the two Scientific Data descriptors (read through Europe PMC, PMC13168504 and PMC12264061); Bao et al. 2024, J Cheminform (doi 10.1186/s13321-024-00911-3; LightGBM, MAE 0.33 in LogS on its holdout).
- Metric: none in the descriptors (no model benchmark; Technical Validation checks the extraction; BigSolDB 2.0 reports the agreement of repeated measurements from different sources, RMSE 0.39 logS and R2 0.90, a noise floor); Bao et al. scored MAE on log g/100 g for the predecessor data; so the fallback `rmse` on the log solubility; inputs none.
- Risks for /add-dataset: ship one target unit (log mole fraction or log g/100 g; the other is a conversion of the target and goes); source DOI, CAS, PubChem CID, the compound name and the FDA flag are identifiers or provenance, not features; the pure-solvent endpoint rows overlap BigSolDB; repeated measurements from different labs disagree (the noise floor above); solutes and solvents come as SMILES and need descriptors (CLEAN-24); split the record before adding.
- Priority: gap 0 (chemistry, regression, grouped not thin), use case 0 (approximate), source +, shape + (175,166 values, 810 solutes, grouped), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the dead-link check of the curator's Zotero collection; the curator's Zotero collection, item 50: "An Ensemble Model for Molecular Solubility Prediction Across Aqueous and Organic Solvents"; the curator's Zotero collection, item 72: "A Model-Mediated Stacked Ensemble Approach for Depression Prediction Among Professionals"; the curator's Zotero collection, item 99: "blaiszik/awesome-matchem-datasets".
- as published: 175,166 measured solubility values, 810 solutes, 3,001 solute/binary-solvent systems, 750 binary solvent mixtures, 252-383 K, from 1,115 articles; one CSV of 41 MB with 20 columns (plus a solvent ...; target: solubility of the solute in the mixture at a temperature (log mole fraction, or g/100 g); access: open.
- Why: measured values, large, CC BY 4.0, new (2026). The authors point to it from the BigSolDB 2.0 record. The mixture composition is an input, so it is a different task from mono-solvent solubility. | Large, real, open, and documented in a data paper. | measured target compiled from peer-reviewed articles with a source ...
- Adds: a sibling of the first-pass hit bigsoldb_2_organic_solubility (same group, separate dataset, not a version). Caveats: compiled from many papers (noise between labs); solutes as SMILES need featurizing; split grouped by solute. | Already proposed by zotero_04 (bigsoldb_2) and awesome_chem_1 ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the record holds MixtureSolDB; BigSolDB 2.0 needs its own record.
