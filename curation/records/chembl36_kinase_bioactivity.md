---
unique_name: chembl36_kinase_bioactivity
name: ChEMBL 36 human kinase bioactivity (kinase-affinity-baselines)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '2026'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/jmabbott40/kinase-affinity-baselines
- https://doi.org/10.64898/2026.04.20.719590
- https://www.ebi.ac.uk/chembl/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: about 353,000 curated compound-kinase potencies from ChEMBL 36 (206,000 compounds, 507 human kinases) with a scaffold split, the QSAR-TID task on a current release; the curated table is not deposited, so it has to be rebuilt with the published pipeline.
- Source: the data is ChEMBL (EMBL-EBI), release 36; the cut is J. Abbott, "kinase-affinity-baselines" (GitHub jmabbott40/kinase-affinity-baselines, MIT, created 2026-03-12) with the bioRxiv preprint doi 10.64898/2026.04.20.719590 (2026). As published (README and docs/data_card.md): "Raw records 501K", "Curated records 353K", "Unique compounds 206K", "Unique targets 507", "Murcko scaffolds 33,808"; IC50 80%, Ki 15%, Kd 5%, as pActivity (-log10 M); single-protein human kinase targets, exact values only, assay confidence >= 7, pChEMBL present, RDKit salt removal and neutralisation, the median of duplicates with a noise flag. A row is a canonical SMILES, a kinase ChEMBL id and pActivity.
- Use case: a medicinal chemist ranks candidate compounds by predicted potency on a kinase before synthesis or assay; the README frames its evaluation as "relevant to real drug discovery prioritization". Fit direct. Regime grouped by Murcko scaffold, the split the source calls "realistic" (it also reports random and kinase-subfamily holdout splits).
- Siblings and duplicates: `qsar_tid_11` (`Yes`) and `qsar_tid_10980` (`TBD -> Yes`) are per-target ChEMBL cuts of MetaQSAR (about 2015) as FCFP bits; `papyrus_bioactivity` (candidate of this run, Papyrus from ChEMBL 34 and other sources) overlaps in kinase rows; `chembl206_estrogen_receptor` and `chembl2034_glucocorticoid_receptor` are other ChEMBL target cuts. All end at ChEMBL, so the curator decides which cuts enter (PROV-6); a pooled kinase table with the target as a feature is a different shape from one target per dataset. External collections: none known.
- Better data: found as better data for `qsar_tid_10980` and `qsar_tid_11`, and from the curator's Zotero collection (item 172); no further search this round.
- Papers and pages: the preprint (not read beyond the repository), the repository's data card and project report; ChEMBL (Mendez et al. 2019, Nucleic Acids Res 47:D930).
- Metric: the source compares every model and split by RMSE ("Regression Performance (RMSE, mean ± SD across 5 seeds)", README) and lists MAE, R², Pearson and Spearman beside it: `rmse`, its ranked criterion and the fallback (MET-5, MET-8); inputs none.
- Risks for /add-dataset: rebuild from ChEMBL 36 with the MIT pipeline (the scout found the Zenodo DOI dead, not rechecked); IC50, Ki and Kd share one target ("Combining them adds noise", data card), so keep the activity type as a column; keep SMILES and compute descriptors rather than ship fingerprint bits (CLEAN-24); stereoisomers collapse in 2D (LEAK-17); 77.3% of rows are active at pActivity >= 6.
- Priority: gap 0 (chemistry and regression are not thin), use case +, source + (ChEMBL; a documented cut), shape + (353,000 rows, scaffold groups), risk - (a rebuild, overlap with other ChEMBL cuts).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `qsar_tid_10980`, `qsar_tid_11`; the curator's Zotero collection, item 172: "Systematic Benchmarking of Kinase Bioactivity Models Across Splitting Strategies and ...".
- as published: compound-kinase measurements; 352,874 rows; 205,747 compounds x 507 human kinases; ECFP4 2048-bit fingerprints + target; ChEMBL 36; target: pActivity (-log10 IC50/Ki/KD), regression; access: open.
- Why: Same kind of task as the QSAR-TID sets (ChEMBL bioactivity from fingerprints) on a current ChEMBL release, with a documented curation (exact values, confidence >= 7, median of duplicates) and a scaffold-grouped regime. The curated table is not deposited (Zenodo DOI 404), so it must be rebuilt from ChEMBL with the MIT ...
- Adds: Much larger and newer than the per-target QSAR-TID sets (ChEMBL ~2015), multi-target, a scaffold split
