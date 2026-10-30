---
unique_name: dataset_from_uncertainty_guided_model_selection_for_tabular_foundation_models_in_biomolecule_efficacy_prediction
name: Dataset from Uncertainty-Guided Model Selection for Tabular Foundation Models in Biomolecule Efficacy Prediction
checked_by:
- Myunghwan
data_foundry_status:
- WIP (DF)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 3
decision_markers:
- Data Requested
tags:
- Non-IID (Grouped)
collections:
- New (BeyondArena)
year: '2005'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://arxiv.org/abs/2510.02476
- https://doi.org/10.1038/nbt1118
v2_path: datasets/_dev/tabarena-v0pt2/dataset_from_uncertainty_guided_model_selection_for_tabular_foundation_models_in_biomolecule_efficacy_prediction/dataset.py
source_row: 865
type_adapter_id: curation-record-v1
---

## Comments

**Current review status (AI, 2026-10-28):** Final ship explicitly approved in the current conversation. Prior individual decisions and completed qualification remain; this new approval supersedes the previously pending overall verdict.

CC (2026-10-28, Myunghwan): "ship for siRNA." Explicit final scientific inclusion of the current reviewed 2,431-row/266-predictor Huesken reporter-assay task, retaining original normalized activity, RMSE and unchanged gene-held-out folds. Earlier scope clarification remains historical; this new explicit ship settles overall inclusion. No build, commit or publication requested.

**Current review status (AI, 2026-10-27):** Add-dataset follow-through is complete; final review-added-datasets verdict is pending. Earlier assertions of scientific inclusion/ship below are superseded agent interpretations, not current curator authority.

CC (2026-10-27, Myunghwan): Clarified that the earlier instruction meant completing tabarena-add-dataset after review for both Youth employment and siRNA, not a final ship verdict. The limited-gene warning and independently confirmed 2005/grouped metadata remain settled. Final overall inclusion is unconfirmed.

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

CC (2026-10-26, Myunghwan): Requested the siRNA efficacy add-dataset stage; this is not a final ship or build decision.

**Assessment (AI, 2026-10-26):** Actual-data source reconstruction uses the corrected Huesken 2005 Table 3, 2,431 observed guides across 30 source species/gene groups. The OligoFormer raw copy omits 70 UBE2H guides and assigns NAS 18412 a human target window although the original marks it rodent. Restored from Table 2 and Table 3 species flags; the reusable loader no longer depends on that copy. Keep original normalized activity, not the processed copy's division by 1.341. Qualification and independent panel are in progress; prior screening claims remain historical. Priority 4: gap + (biology/grouped), use case + (library design), source + (corrected primary supplement), shape + (2,431 rows and grouped features), risk - (10 held-out genes per fold and assay transfer limits).

**Assessment (AI, 2026-10-26):** Final add-stage result. Added for Myunghwan's added-dataset review, not final inclusion or build. Corrected Huesken 2005 data: 2,431 guides, 30 species/gene groups, 266 predictors (88 categorical, 178 numeric). The exact primary measured labels, guide chemistry, target context and all 30 native gene-held-out splits have independent checks. Final task probe: LightGBM mean RMSE 0.161820 versus training-mean 0.202355, better in every split; random forest 0.164815 and linear 0.175294; no task-probe flags. Dataset check: 0 errors, one still-unaccepted groups_test_groups_few warning (ten genes per test fold). Repeated partitions reuse the same thirty genes; pooled row scoring is not a demonstration of within-gene shortlist utility or endogenous/clinical transfer. Complete independent/blind ten-role panel recommends ship after documentation and curator dispositions. Descriptor terminal-sign and enthalpy-rounding conventions are now explicit; final documentation edits preserve exact data, dtypes, model inputs, metric and split memberships, with a reuse receipt rather than another model run.

Priority corrected from the earlier AI proposal to 3: start 1 + corrected primary source 1 + shape 1. Current accepted-inventory factors give no biology/grouped gap point, the reporter use is approximate rather than direct, and no qualifying risk deduction is established. No human priority-4 decision is overridden. Year 2025 versus source 2005, New IID versus current grouped task, and the residual '?' split entry remain explicit REVIEW field rows for curator marks; they are not silently changed. The real historical Data Requested entry is retained: Huesken has now been obtained, whereas the reuse paper's patent-derived Target1/Target2 data and identities were not reconstructed here. Its assertion of public patent sources does not support our earlier blanket 'not public' wording. Original full methods and redistribution terms remain unconfirmed; the inspected corrigenda, corrected supplement and later paper do not establish a uniquely mandated original metric, so RMSE remains a qualified fallback. Full evidence and historical notes are preserved; no warning acceptance or human semantic verification is claimed.

CC (2026-10-26, Myunghwan): Approved scientific inclusion. In this case 30 genes are acceptable; even five test genes can be acceptable when the number of test records is sufficient. Confirmed grouped prediction for new gene IDs (OOD in that sense), and asked whether the tag fits. Existing ten-gene test folds are retained; no repartitioning was requested. The original chat words and scoped marks are preserved in the review history.

CC (2026-10-26, Myunghwan): Metadata `tag`: update; Non-IID (Grouped), meaning unseen gene IDs.

CC (2026-10-26, Myunghwan): Metadata `year`: update; 2005 original-source year.

**Assessment (AI, 2026-10-26):** Applied the actual curator approval and accepted `groups_test_groups_few` with the case-specific rationale and multi-family grouped evidence. No fixed minimum number of genes is imposed for this row-level continuous target; no blanket row-count-only rule is introduced. The unchanged folds have ten test genes and 648-942 records. Confirmed grouped cold start; SPLIT-2 already covers unseen IDs under Non-IID (Grouped), with no separate OOD vocabulary. Year/tag choices are applied only where explicitly marked; unanswered rows remain in REVIEW. Exact data, dtypes, target, metric and ordered split memberships are preserved, so completed model qualification is reused. Scientific approval does not authorize build, commit or redistribution.
