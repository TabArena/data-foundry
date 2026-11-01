---
unique_name: leffingwell_odor_musk
name: Leffingwell Odor Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2020'
domain: chemistry & material science
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.4085098
- https://github.com/pyrfume/pyrfume-data/tree/main/leffingwell
- https://arxiv.org/abs/1910.10685
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 3,522 perfumery molecules with expert odor descriptors (113 binary labels) and structures, a real structure-odor task; but the record's musk label has 20 positives, so it is no better data for `musk`, and a frequent descriptor or the label set must be chosen.
- Source: John Leffingwell's PMP 2001 database, curated by Sanchez-Lengeling, Wei, Lee, Gerkin, Aspuru-Guzik and Wiltschko (Google), Zenodo 10.5281/zenodo.4085098 (v1.0, 2020-10-13, CC BY-NC 4.0, files restricted: access on request): "curated and cleaned a dataset of 3523 molecules"; open copy in pyrfume-data `leffingwell/` (manifest: "Originally produced by John Leffingwell and cleaned by Sanchez-Lengeling et al"). Previewed: `behavior.csv`, 3,522 molecules x 113 descriptor columns (0/1); `leffingwell_data.csv` with chemical_name, smiles, database_id, cas, odor_data (the free-text description), odor_labels_filtered, labels_train/test, labels_cv0-cv4 (the authors' splits). Positives per descriptor (counted on behavior.csv): fruity 1,391, green 907, sweet 825, floral 553, fatty 407, herbal 406, ..., musk 20 (the minimum, with catty, horseradish, leathery and radish).
- Use case: a flavour and fragrance chemist screens candidate molecules for an odor before synthesis and panel tests; the paper names "manufacture of synthetic fragrance" among its applications, no actor or decision; fit approximate. Regime grouped by scaffold (SPLIT-31) or IID (the authors used iterative stratification); the add stage decides.
- Siblings and duplicates: `musk` (`Yes`, DF: Yes; UCI Musk v2, 102 molecules, 39 musks, conformation features scored per molecule): another source and another kind of feature, not a duplicate (PROV-4). No other odor record (grep odor, olfact, goodscents, pyrfume). External collections: pyrfume; listed in awesome-chemistry-datasets; the curator's Zotero item 81 (TabPFN-Wide) uses it.
- Better data: found as better data for `musk`; no further search this round. Counted here: musk has 20 positives among 3,522 molecules (about 4 per test fold of five), so for the musk label this is not better data than `musk` itself.
- Papers and pages: Sanchez-Lengeling et al., "Machine Learning for Scent", arXiv 1910.10685 (2019; read): its benchmark merged GoodScents (3,786) and Leffingwell (3,561) into 5,030 molecules and 138 descriptors with at least 30 molecules each, so the released file is a part of the paper's data; Lee et al. 2023 (the principal odor map, Science) used the merged set (not read).
- Metric: the paper: "we primarily compare models on mean AUROC, averaged across odor descriptors" (Sec. 5), a deliberate choice (MET-5), so `roc_auc` for one descriptor; F1, precision and recall are reported beside it. Inputs none.
- Risks for /add-dataset: the record's named target fails TP-5 (20 positives), so the definition takes a frequent descriptor (fruity, green, sweet, floral) or the label set (`Multi-target`, CLEAN-18); labels come from free text ("not described as musky" is not "not musky"), and the set "is biased away from malodorous compounds" (paper Sec. 4); SMILES only, so the structure ships as RDKit 2D descriptors as for `apistox`; repeated structures across salts or isomers (LEAK-17); the non-commercial licence is no criterion (EV-4).
- Priority: gap 0 (chemistry not thin), use case 0 (no actor), source + (paper, Zenodo record with a readme), shape + (3,522 molecules; most descriptors have hundreds of positives), risk - (the musk label too small, free-text labels).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `musk`; the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 81: "TabPFN-Wide: Continued Pre-Training for Extreme Feature Counts".
- as published: 3,523 molecules with 113 expert odor descriptors (multi-label 0/1), SMILES and the authors' train/test/CV splits, plus precomputed featurizations; target: an odor descriptor per molecule (for example musk), 0/1; access: open (pyrfume-data GitHub copy; the Zenodo files need an access request); license CC BY-NC (non-commercial), check before use, request.
- Why: already found by the 2026-10-30 better-data scouting (scout_09, for musk) and still without a record; listed here because the chemistry list carries it too | Same target as musk (does a molecule smell musky) and the same unit (the molecule), with features computed from the structure, known before any odor test. ...
- Adds: see scout_09: about 35 times the molecules of musk, with structures. Note on access: the Zenodo record is marked restricted (access request); the open copy is pyrfume-data, licence CC BY-NC | About 35 times more molecules; the structure (SMILES) is given, so standard descriptors and a scaffold split are possible and ...
