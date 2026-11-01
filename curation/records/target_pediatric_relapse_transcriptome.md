---
unique_name: target_pediatric_relapse_transcriptome
name: 'TARGET pediatric cancers: relapse from diagnostic tumour RNA-seq (GeneICL task TARGET::relapse)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Many features
original_source: GOV Website
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://portal.gdc.cancer.gov/projects/TARGET-NBL
- https://github.com/BoevaLab/GeneICL
- http://arxiv.org/abs/2610.08694
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and papers, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: GeneICL's `TARGET::relapse` task, 2,046 tumour samples of NCI's TARGET paediatric cancer projects labelled for relapse from RNA-seq (log1p-CPM over 20,021 genes); open data and a large clinical-outcome cohort for expression, but the label logic sits in code GeneICL did not ship, so the target must be rebuilt from TARGET's clinical files with censoring and sample types in mind.
- Source: the NCI TARGET program (Therapeutically Applicable Research to Generate Effective Treatments), served by the Genomic Data Commons. GDC API (2026-10-31): nine TARGET projects (AML 2,492 cases, ALL-P2 1,587, NBL 1,132, WT 652, OS 383, ALL-P3 191, RT 69, ALL-P1 24, CCSK 13) and 4,374 gene expression quantification files, all open access (AML 3,227, ALL-P2 532, NBL 162, WT 136, ALL-P3 135, OS 88, RT 69, CCSK 13, ALL-P1 12). The task: Bohl, Theus, Wissel and Boeva, "GeneICL: A Tabular Foundation Model for Bulk Transcriptomics" (arXiv 2610.08694, 2026-10-06; abstract read: 80 outcome tasks), repository github.com/BoevaLab/GeneICL: `eval/data/benchmark/index.json` lists the dataset `TARGET` with 4,149 samples and three tasks, `TARGET::relapse` (classification, n = 2,046), `TARGET::mrd` (regression, 453) and `TARGET::inss_stage` (159); `build_data.py` "reuses the task registry + data loaders of the upstream curation code (GenePFN eval/, not part of this repo)" and "reimplements no label logic", so the projects, the samples and the relapse definition behind the 2,046 are not documented.
- Use case: a paediatric oncologist at diagnosis assigns a risk group that sets treatment intensity (in AML, for example, a transplant in first remission), using the relapse risk; ours to state (GeneICL names clinical outcome prediction from expression in general); fit approximate (tumour types and treatment protocols pooled). Regime grouped: by project for a new disease, and by patient when a patient has several samples (GeneICL's harness groups folds on a task's `group` when it has one; whether `TARGET::relapse` has one was not checked).
- Siblings and duplicates: `treehouse_pediatric_tumor_type` (`TBD -> Yes`, 3; UCSC Treehouse's compendium, 1,340 of its datasets from TARGET, for a diagnosis task: another target, PROV-7); `beataml2_ex_vivo_drug_response` (`TBD -> Yes`, 2; adult AML, BeatAML, which GeneICL also uses); expression-outcome records `early_sepsis_mortality_transcriptome` (`TBD -> 2nd Tier`, 1) and `commpass_myeloma_survival` (`TBD -> 2nd Tier`, 1); the TCGA records (adult tumours). No record of TARGET outcomes (grep: GeneICL, TARGET-, neuroblastoma). External collections: GeneICL's benchmark suite (52 tasks).
- Better data: from the curator's Zotero collection (item 300, the GeneICL paper); no further search this round.
- Papers and pages: the GeneICL paper and repository; the GDC TARGET project pages; the per-disease TARGET papers (not read).
- Metric: GeneICL tunes its classical baselines by "mean inner AUROC / R²" and logs ten classification metrics (`auroc`, `auprc`, F1, balanced accuracy, accuracy, MCC, NLL, Brier, ECE; eval/benchmark/README.md); the paper's ranking metric was not read; so `roc_auc`, which is also the fallback (MET-5, MET-8); inputs none.
- Risks for /add-dataset: build the label from TARGET's clinical data with a fixed horizon, dropping patients censored before it (USE-5); the GDC's structured recurrence fields are sparse (`follow_ups.progression_or_recurrence` "yes" for 359 of 6,543 cases), so the per-project clinical files are the source; TARGET holds samples taken at relapse (GDC: 598 "recurrent blood derived cancer - bone marrow", 47 from peripheral blood, 35 "recurrent tumor"), and only diagnostic samples may enter (USE-3, LEAK); several samples per patient (SPLIT-24); the project may carry much of the signal (fit a project-only baseline, TP-4); 20,021 gene columns, normalised per sample (log1p-CPM), so no transform across samples (LEAK-30 not triggered by GeneICL's file).
- Priority: gap 0 (medical & healthcare and binary classification are not thin), use case 0 (ours), source + (NCI's documented program, open data, the task's code public), shape + (2,046 samples, grouped by project), risk - (an undocumented label, relapse-time samples, censoring).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 300: "GeneICL: A Tabular Foundation Model for Bulk Transcriptomics".
- as published: tumour samples: 2,046 with a relapse label in GeneICL's index, across TARGET's pediatric tumour projects (which ones not checked). GDC has open-access gene expression quantification (about 20k ...; target: relapse after first-line treatment (binary), from expression at diagnosis; access: open.
- Why: The largest clinical-outcome task in the GeneICL suite, from open NCI data.
- Adds: Thousands of rows rather than tens, and tumour type gives a grouped split. To check: which projects, how relapse and follow-up are defined (censoring), whether clinical files agree across projects, and whether tumour type alone explains most of the signal.
