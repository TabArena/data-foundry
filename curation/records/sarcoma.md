---
unique_name: sarcoma
name: SARC
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: Website
year: '2018'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
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

## Reference

N. Rappoport and R. Shamir. Multi-omic and multi-view clustering algorithms: review and cancer benchmark. Nucleic Acids Research, 46(20):10546–10562, Oct 2018. URL https://doi. org/10.1093/nar/gky889.
