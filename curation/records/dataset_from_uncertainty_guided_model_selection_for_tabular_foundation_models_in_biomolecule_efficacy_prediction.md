---
unique_name: dataset_from_uncertainty_guided_model_selection_for_tabular_foundation_models_in_biomolecule_efficacy_prediction
name: Dataset from Uncertainty-Guided Model Selection for Tabular Foundation Models in Biomolecule Efficacy Prediction
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
decision_markers:
- Data Requested
tags:
- New IID
- AI-Filled (Verify)
collections:
- New (BeyondArena)
year: '2025'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://arxiv.org/abs/2510.02476
- https://doi.org/10.1038/nbt1118
source_row: 865
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 4: siRNA knockdown efficacy on the Huesken et al. (2005) library, 2,361 siRNAs over 29 target mRNAs, a grouped regression in a thin domain; the paper's two patent-derived sets are not public.
- Source: the efficacy data was first published by Huesken et al. (2005), "Design of a genome-wide siRNA library using an artificial neural network", Nature Biotechnology (doi:10.1038/nbt1118, supplementary data); this record's paper, Li, McCarthy, Zhang and Young (2025), arXiv:2510.02476, re-uses it ("We divided the Huesken dataset (2361 data points) into 29 subsets, each corresponding to a different mRNA target") and adds Target1 (patents of institutions A, B, C: 295, 366, 9 points) and Target2 (a patent of institution D: 252 points), with no data availability statement. So `year` 2025 is the re-use; the data dates from 2005 (left as is, metadata is filled only where empty). Features in the paper: 574 per siRNA (361 one-hot positions of a 57-nt window, 189 trimer counts, 24 thermodynamic values); target the knockdown efficacy.
- Use case: a researcher designing siRNAs for a new gene picks the candidates to synthesise and test (Huesken: a genome-wide library designed by a network); fit direct; regime grouped by target mRNA (a new gene at prediction time; the paper used 5-fold CV on Huesken and few-shot on new targets).
- Siblings and duplicates: no record of Huesken or siRNA data (grep: huesken, sirna, knockdown). External collections: none known; Huesken is a standard set of siRNA efficacy predictors.
- Papers and pages: Huesken et al. 2005; Li et al. 2025 (TabPFN on sequence features beats specialised siRNA predictors, their claim).
- Metric: MAE and Pearson correlation reported side by side, correlation emphasised in the conclusion but not named as the criterion (MET-5); Huesken's own evaluation not read; so the fallback `rmse` (MET-8) unless the curator takes Pearson.
- Risks for /add-dataset: sequence data (SEL-12): one-hot and k-mer features where sequence models may win (the paper argues tabular wins); the features are a design choice of ours, to be derived from the sequences as published; the group column (target mRNA) must ship; the `New IID` tag contradicts the grouped regime; Target1 and Target2 not available (`Data Requested`, 14/03/2026).
- Priority: gap + (biology & life sciences and grouped are thin), use case + (siRNA design), source + (Nature Biotechnology paper), shape + (2,361 rows, grouped structure), risk - (sequence modality, SEL-12).

Dataset(s) from a 2025 arXiv paper on tabular foundation models for biomolecule efficacy prediction; this is a genuine tabular predictive task (efficacy regression/classification on molecular descriptor features) and explicitly relevant to tabular ML. The record notes the data was preprocessed from prior work, was requested on 14/03/2026, and could possibly be reconstructed manually. Risks: the features may be derived/transformed descriptors, and a grouped (by scaffold/assay) split may be required. A human must verify data availability, that the features are not lossy/irreversible transforms, the exact target, and the appropriate split.

---

Their data could be used; it is from another work and has been preprocessed.

Lennart: requested their versions of the dataset for benchmarking on 14/03/2026. But we could also likely reproduce one/some of their data state manually
