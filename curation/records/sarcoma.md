---
unique_name: sarcoma
name: SARC
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
decision_markers:
- Selection Bias
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: Website
year: '2018'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://acgt.cs.tau.ac.il/multi_omic_benchmark/download.html
v2_path: datasets/_dev/tabarena-v0pt2/sarcoma/dataset.py
source_row: 783
type_adapter_id: curation-record-v1
---

## Comments

used in the TabPFN-Wide paper. from their download instructions: to map the methylation probe IDs to gene symbols, download the file from `https://webdata.illumina.com/downloads/productfiles/humanmethylation450/humanmethylation450_15017482_v1-2.csv`

**Assessment (AI, 2026-10-07):** No reason for `DF: Suspended` is recorded here or in git. TabPFN-Wide (arXiv 2510.06162v1, Sec. 5) classifies `histological_type`, so `problem_type` should be Multiclass Classification. That field is the submitted diagnosis: the TCGA sarcoma study (Cell 2017) confirmed 206 cases by expert review, excluded the others (QC failures, "3 probable melanomas", uncertain types) and reclassified 20. Added as `datasets/_dev/tabarena-v0pt2/sarcoma/` with the reviewed type from the study's GDC master patient table: 201 patients (the 5 MPNST dropped; LMS 80, DDLPS 50, UPS 44, MFS 17, SS 10) and 25,971 omic features. Open: the study treats UPS and MFS as one spectrum.

CC (2026-10-12, Lennart): Kept in TabArena v0.2 after the task-probe review (flag `few_minority`, multiclass). Synovial sarcoma has 10 rows, 3-4 per test fold. They are 5% of the test rows and 6.5% of a random forest's log loss (0.64 against 1.41 for the class shares). Too Small is for a task whose scored units are a handful; one rare class of the source's own labels that does not decide the score is part of the task.

CC (2026-10-19, Lennart): for the next pass, rebuild the methylation block from the GDC's per-sample beta values: the source kept 5,000 probes, by our notes chosen by variance over all patients and imputed with k-nearest neighbours over all patients. Kept as is until then.

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap + (problem_type multiclass_classification), use case -, source +, shape -, no known risk. A very wide (26k features), tiny (201 patients) multiclass omics task that covers the wide-data regime; its use case is invented.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes; applied: the 61 `Methy_rs*` SNP genotype probes dropped, fit set to approximate (five confirmed types stand in for every referred sarcoma), the label note says the review required 12q15 copy-number gain for DDLPS (not shipped, so SEL-5 is not triggered), the source's all-patient preprocessing written as a kept potential leak, and a `splits_comment` added. The use case is real (molecular sarcoma typing, Koelsche et al. 2021), not invented. Open: merge MFS and UPS, and IID or site-grouped split (REVIEW.md issues 3 and 4). Priority 3: gap +, use case -, source +, shape -, risk 0 (gap: multiclass; use case: fit approximate; shape: 201 patients; risk: the leak is weak and kept by the curator, and the open issues are weighing calls, not a leak or an unclear target).

CC (2026-10-21, Lennart): "let us stay with direct fit if the task (without leakage) would be a direct fit and only move to approximate fit if we had to change a lot to avoid the leak"; USE-8 amended. The fit stays approximate for the closed set of five confirmed types; the kept preprocessing over all patients is no longer a reason for it.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — The source (Rappoport & Shamir 2018) is a clustering benchmark without a label, and the TCGA study (Cell 2017) defines no prediction metric. The task paper the definition cites, TabPFN-Wide (Kolberg et al. 2025, arXiv 2510.06162), reports AUROC and accuracy on COAD/LGG/BRCA/GBM/OV, but SARC 'is only used for attention analysis' (Table 1 caption), so no metric is defined for this task.

CC (2026-10-22, Lennart): issue 3: merge myxofibrosarcoma and undifferentiated pleomorphic sarcoma. Issue 4: keep the IID split by patient. Record field `problem_type` takes the definition's value (multiclass).

**Assessment (AI, 2026-10-22):** four classes: leiomyosarcoma 80, undifferentiated pleomorphic sarcoma or myxofibrosarcoma 61, dedifferentiated liposarcoma 50, synovial sarcoma 10 (the TCGA study's single spectrum and the methylation classifier's one class, Koelsche et al. 2021). Random forest log loss 0.650 to 0.469, macro ROC AUC 0.958 to 0.984; the only probe flag is `few_minority` (synovial sarcoma, 3 per test fold). Holding whole sites out now raises the forest's log loss from 0.46 to 0.58 (stated in `splits_comment`). The best single feature (MDM2) reaches skill 0.24 against 0.75 for the best model. dataset check: 0 errors, 0 warnings. REVIEW.md removed (nothing left open). Not built yet.

## Reference

N. Rappoport and R. Shamir. Multi-omic and multi-view clustering algorithms: review and cancer benchmark. Nucleic Acids Research, 46(20):10546–10562, Oct 2018. URL https://doi. org/10.1093/nar/gky889.
