---
unique_name: ready_biodegradability_huang_zhang
name: Aerobic ready and inherent biodegradation of organic chemicals (Huang & Zhang 2022)
checked_by:
- AI (UNVERIFIED)
- Andrej
suggestion: TBD -> Yes
priority: 2
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
original_source: Other
year: '2022'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.1021/acs.est.2c01764
- https://github.com/pkoerner6/Prediction-of-Aerobic-Biodegradability-of-Organic-Chemicals
- https://pubs.rsc.org/en/content/articlehtml/2024/em/d4em00431k
- https://doi.org/10.1039/d4em00431k
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: ready biodegradability (yes/no) of about 6,100 chemicals with SMILES, compiled (per the run's Assessment) from REACH screening-test records, the task of `qsar_biodeg` on about six times the chemicals; a later study shows label noise and identifier errors in it, so the curator chooses between the original and its curated version.
- Source: Huang and Zhang, "Classification and Regression Machine Learning Models for Predicting Aerobic Ready and Inherent Biodegradation of Organic Chemicals in Water", Environmental Science & Technology 56(17), 2022 (doi 10.1021/acs.est.2c01764; the paper and its supporting information were not reachable, 403). As carried by Körner et al.'s repository (GPL-3.0): `datasets/external_data/class_original.csv` (1.8 MB; header previewed: name, name_type, cas, source = `ClassDataset_original`, smiles, y_true, plus pKa and speciation columns Körner added), `class_external.csv`, `class_all.csv`, and `Huang_Zhang_RegressionDataset.xlsx` (2.0 MB); curated versions in `datasets/curated_data/` (`class_curated_final.csv`, `class_curated_scs.csv`, `class_curated_biowin.csv`). The sizes in the Assessment below (6,139 substances; 12,750 regression records on 6,032 substances) come from the run, not re-counted.
- Use case: a registrant or regulator screens a chemical for persistence under REACH before or instead of an OECD 301 test (the label is the outcome of such tests); fit direct for a new chemical, approximate until Huang and Zhang's own statement is read. Regime grouped on the Bemis-Murcko scaffold, as for every molecule set with exact structures (SPLIT-31 as amended 2026-10-26).
- Siblings and duplicates: `qsar_biodeg` (`Yes`, TabArena v0.1: Mansouri et al. 2013, 1,055 chemicals with 41 descriptors) and its copy `qsar_biodegradation` (`No`); another compilation of overlapping test data, so not a duplicate (PROV-4), but some chemicals will be in both. Körner's curated sets are versions of this one (PROV-6). External collections: none found.
- Better data: found as better data for `qsar_biodeg`; no further search this round.
- Papers and pages: Huang and Zhang 2022 (ES&T); Körner, Glüge, Glüge, Scheringer, "Critical insights into data curation and label noise for accurate prediction of aerobic biodegradability of organic chemicals", Environmental Science: Processes & Impacts 2024 (doi 10.1039/d4em00431k), whose README reports correcting "mismatched chemical identifiers and data leakage between training and test sets" and removing chemicals with high variance across studies, balanced accuracy 80.9% before and 94.2% after filtering possibly noisy labels, and warns that filtering may have removed difficult-to-learn substances.
- Metric: Huang and Zhang's metric not read (paper unreachable); Körner et al. name balanced accuracy, a threshold metric with no threshold or costs fixed (MET-6), so the fallback `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: label noise (one chemical tested several times with conflicting results; how the original resolved them) and the CAS-SMILES mismatches Körner found: repair from the origin (PROV-13) or ship the curated version, but not the label-noise-filtered one, which drops the hard cases on purpose (a target the curation chose, TP-6); the Körner speciation columns are his additions, not the source's; the chemicals shared with `qsar_biodeg`; descriptors computed from SMILES per fold, never from all rows (LEAK-29). The regression set (percent degradation by guideline and duration) mixes test types and is a second task to judge on its own.
- Priority: gap 0 (chemistry, binary, grouped are not thin), use case 0 (not read from the source), source + (a peer-reviewed compilation; the REACH origin per the run, not read), shape + (about 6,100 chemicals with structures, scaffold groups), risk - (label noise and identifier errors shown by Körner et al.).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `qsar_biodeg`.
- as published: classification: 6,139 substances (ready biodegradable yes/no); regression: 12,750 test records on 6,032 substances (percent degradation with test guideline and duration); compiled from ECHA REACH ...; target: ready biodegradable (yes/no) from OECD 301-type screening tests; access: open (copies in Koerner et al.'s repository, datasets/external_data/class_original.csv and Huang_Zhang_RegressionDataset.xlsx, GPL-3.0; the ES&T supporting information as the original was not opened).
- Why: Same target (ready vs not ready biodegradable) and unit (the chemical) as qsar_biodeg, with structure-derived features known before the test
- Adds: About 6 times more chemicals (6,139 against 1,055), a newer and regulatory source (REACH dossiers), structures given (RDKit descriptors and a scaffold split as for the other SMILES datasets); Koerner et al. 2024 publish a curated version with a label-noise analysis

**Assessment (AI, 2026-11-12):** pair with `qsar_biodeg` open (Andrej's decision on its review, 2026-11-12): when this set is added, match its chemicals to qsar_biodeg's 1,050 on canonical SMILES and CAS-RN, report the share of qsar_biodeg's chemicals found here and their class agreement, and put the pair to the curator; qsar_biodeg is retired if this set holds most of its chemicals with the same class.
