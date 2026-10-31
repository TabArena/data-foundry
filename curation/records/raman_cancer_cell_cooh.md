---
unique_name: raman_cancer_cell_cooh
name: Cancer Cell ((COOH)2)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- TBD
- Too Small
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
collections:
- RamanBench
original_source: Kaggle
year: '2019'
domain: medical & healthcare
problem_type: Multiclass Classification
original_data_state: Other
source_links:
- https://doi.org/10.1016/j.snb.2020.127660
- https://www.kaggle.com/datasets/andriitrelin/cells-raman-spectra
- https://arxiv.org/abs/2605.02003
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, the release file listings and a two-column preview of the data, NOT from a build. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: SERS spectra of culture media from melanoma, melanocyte, fibroblast and control samples, released by the authors on Kaggle, but 8-9 samples per class, no sample column, and a 12-class label that crosses the cell type with the serum condition.
- Source: first released by the authors on Kaggle, andriitrelin/cells-raman-spectra "Cells Raman Spectra" (files of 2019-08-04 and 2019-10-24; README: "collected in the University of Chemistry and Technology, Prague", CC BY-NC-SA 4.0); paper Erzina et al., "Precise cancer detection via the combination of functionalized SERS surfaces and convolutional neural network with independent inputs", Sensors and Actuators B 308:127660, 2020 (paywalled, not read). As published: 12 folders (A, A-S, G, G-S, HPM, HPM-S, HF, HF-S, ZAM, ZAM-S, DMEM, DMEM-S) with three CSVs each, one per gold nanourchin functionalisation (NH2, COOH, (COOH)2); rows are spectra of 2,090 points (100-4278 cm-1), "background-subtracted, unfiltered, unnormalized"; the README table gives "No of samples" 8 or 9 per label (106 in all) and the files carry no sample column.
- Use case: "cancer cell determination by analysis of surface enhanced Raman spectra of the cell medium" (Kaggle, Context); a lab would classify cells from their conditioned medium. Fit approximate: cell lines and primary cultures, and the 12 labels cross six cell types with 10% or 0% serum, an experimental condition rather than something to predict (USE-5). Regime grouped by culture sample: the spectra of one sample share it, and the Kaggle goal is to "map triple [NH2, COOH, (COOH)2] to the corresponding class".
- Siblings and duplicates: the three functionalisations are one dataset (the COOH, (COOH)2 and NH2 cuts are aliases of this record; the source's task uses all three together, PROV-6); the record's name ("Cancer Cell ((COOH)2)") is one of the cuts. Other SERS records of the run: `raman_adenine_colloidal_gold`, `raman_hair_dyes_sers`, `raman_serum_prostate_cancer`. External collections: RamanBench ("Cancer Cell (COOH)", "((COOH)2)", "(NH2)", 627-633 spectra each).
- Better data: a candidate of the benchmark RamanBench (arXiv 2605.02003); no further search in this run.
- Papers and pages: the Kaggle page and README; the paper (not read; the raman-data loader summarises it as a multi-input CNN on a 75:25 split with "100% validation accuracy", unverified, PROV-16).
- Metric: accuracy per that unverified summary, a habit at best on a random split of spectra (MET-5, MET-6), so the fallback log_loss on the label chosen. Inputs: a sample id, which does not ship.
- Risks for /add-dataset: no sample id: recover it exactly from the file order or ask the authors, otherwise SPLIT-25 retires it; 8-9 samples per label, 1-2 per class in a grouped test fold (TP-5, TP-8): merge to the cell type (17-18 samples each) or cancer against the rest (TP-7); align the three functionalisations per sample if the files allow it; raw spectral bins (SEL-15).
- Priority: gap + (multiclass thin), use case - (no decision named, cell lines), source + (authors' release with README, paper), shape - (106 samples), risk - (no sample id, few samples per class).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 627 spectra x 2,090 wavenumber features; 12 classes (raman-data id: cancer_cell_(cooh)2); target: sample category (cell line x FBS).
- Why: Classify the cell type (melanoma, melanocytes, fibroblasts, control medium; with/without FBS) from SERS spectra of conditioned culture media
- Notes: Raw Raman spectral bins (2,090 wavenumber points, 100-4278 cm-1) as features; SEL-15 judges such signals case by case. One of 3 functionalisation variants (AuMs-(cooh)2) of the same study. Licence CC BY-NC-SA 4.0. ~30 spectra per sample (grouped). HF mirror: ...
