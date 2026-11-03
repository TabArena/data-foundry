---
unique_name: b3db_blood_brain_barrier
name: 'B3DB: a curated diverse molecular database of blood-brain barrier permeability'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
- Many features
original_source: Other
year: '2021'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1038/s41597-021-01069-5
- https://github.com/theochem/B3DB
- https://doi.org/10.6084/m9.figshare.15634230.v3
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and papers, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: B3DB, 7,807 compounds with a BBB+/BBB- label compiled from 50 published sources and grouped by how the label was set, with 1,613 mordred descriptors, CC0; the largest public set for the blood-brain-barrier task of `bbbp_martins`.
- Source: Meng, Xi, Huang and Ayers 2021, "A curated diverse molecular database of blood-brain barrier permeability with chemical descriptors", Sci Data 8:289 (doi 10.1038/s41597-021-01069-5, 2021-10-29; PMC8556334); data at github.com/theochem/B3DB (CC0) and figshare (doi 10.6084/m9.figshare.15634230.v3). As published: a classification table, "7807 molecules with 4956 BBB+ and 2851 BBB−" (7,982 after the repository added "171 BBB+ and 4 BBB-" compounds), and a regression table of 1,058 logBB values; columns compound name, IUPAC name, isomeric SMILES, CID, logBB, BBB+/BBB-, InChI, threshold, reference, group, comment, and "1613 molecular descriptors" (mordred 1.1.1) in the extended files. Label groups: A (1,058, logBB, "The value of −1 is chosen as the threshold value"), B (3,621, "sources that use log BB = −1 as the threshold value, and where all sources agree"), C (3,077, "all sources agree on the categorical label, but the sources that do not report their threshold value"), D (51, two labels, "The most prevalent label is used").
- Use case: "predicting whether a substance crosses the BBB is a key task in lead discovery for CNS drugs" (abstract): a medicinal chemist before synthesis; fit direct. Regime grouped on the Bemis-Murcko scaffold (SPLIT-31).
- Siblings and duplicates: `bbbp_martins` (Martins et al. 2012, about 2,050 compounds; `TBD -> Yes`, priority 3) is the same task; B3DB cites Martins 2012 among the sources using the −1 threshold (ref. 28), so its compounds are probably inside this set (to count in `raw_data/raw_data_summary.tsv`); the curator keeps one (PROV-6 question). `tdc_bbb_martins` is screened `No` (`Duplicate`). The 1,058-compound logBB regression is a second task of the same source (PROV-7), with no record yet. External collections: awesome-chemistry-datasets; B3clf (Meng et al., ChemRxiv 2025) builds on it.
- Better data: from the awesome-chemistry-datasets list and the curator's Zotero collection (item 85); the run recorded it as better data for `bbbp_martins`; no further search this round.
- Papers and pages: Meng et al. 2021 (the data); the GitHub README (versions, a loader).
- Metric: none found (the paper trains no model; the README recommends no split or metric), so the fallback `roc_auc` (MET-8), which MoleculeNet and TDC also use for the Martins task; inputs none.
- Risks for /add-dataset: the label mixes definitions (group C, 39% of the rows, comes from sources that do not report a threshold), and the authors recommend "to incorporate the group categories when using the datasets": a filter or a note (USE-5); `group`, `threshold`, `logBB` and `reference` describe the label and are no features (LEAK); the 1,613 descriptors are computed from the structure (CLEAN-24); BBB+ are 63% of the rows, more than in a screening library (a `Selection Bias` question, as on `bbbp_martins`); stereoisomers kept as isomeric SMILES collapse onto the same 2D descriptors (LEAK-17).
- Priority: gap 0 (chemistry & material science and binary classification are not thin), use case +, source +, shape + (7,807 compounds, 1,613 descriptors), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 85: "Cyber risk and cybersecurity: a systematic review of data availability".
- as published: 7,807 compounds with BBB+/BBB- labels (7,982 from v1.0.0), 1,058 of them with a numeric logBB; compiled from about 50 published sources, with physicochemical descriptors; TSV files; target: blood-brain barrier permeability class (BBB+ or BBB-); logBB for the regression subset; access: open.
- Why: same task as MoleculeNet BBBP and TDC BBB_Martins (items 85 and 93), about four times larger and ten years newer
- Adds: the better data for the BBBP task that the catalogues still list in its old form; check how many labels are thresholded logBB and how many are reported classes, and whether sources overlap
