---
unique_name: hepatitis_c_egypt
name: HEPATITIS_C_EGYPT
checked_by:
- Andrej
- Lennart
suggestion: 'Yes'
priority: 1
tags:
- New IID
collections:
- TabSTAR
original_source: UCI
year: '2019'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/503/hepatitis+c+virus+hcv+for+egyptian+patients
- https://www.openml.org/search?type=data&id=46607
- https://doi.org/10.24432/C5989V
source_row: 676
type_adapter_id: curation-record-v1
---

## Comments

Paper reports pretty good performance, need to pay attention to target leaks. Unclear when the target was collected. Was it really after the features or can features leak the target?

After consulting Dr. GPT, learned that ALT features correspond to future follow-up measurements - temporal leakage. We could use the other features, but that's probably not very useful.

**Assessment (AI, 2026-10-07):** The UCI file (OpenML 46607 is identical) does not behave like patient records. Its columns are independent: 21 of 406 pairs pass the 95% noise band, 20 by chance. The links HCV cohorts show are absent: AST-ALT r = 0.04, RBC-HGB 0.04, the same HGB in men and women, FIB-4 against stage AUC 0.47-0.49 (0.71-0.82 in 19,501 Egyptian biopsies, El-Kassas et al. 2024), and response is unrelated to grade, stage and baseline RNA, its predictors in the creator's own cohort (Kamal et al. 2007). AST and six ALT visits are uniform on 39-128. The stage cannot be predicted (macro AUC 0.48-0.51). Suggest No + AHDS; Data Quality Issue if real values were replaced.

**Open issues (AI, 2026-10-07):** not added; recommended `No` (`AHDS`). No column depends on another, the label
included: generated or replaced data.

1. **Verdict.** Question: keep `Yes`? Evidence (the assessment above): no dependence that HCV data must show is
   present, the values are flat over their ranges, and the stage cannot be predicted from any subset. Implemented:
   not added; the assessment is in this record. Markers, your call: `AHDS` fits; add `Data Quality Issue` too if you
   read it as a real table with replaced values, which is as likely as a fully synthetic one (the creators ran
   genotype-4 cohorts with this design: RNA at weeks 4 and 12, end of treatment and 24 weeks after; Kamal et al.
   2005, 2007). Alternative: add the checked definition that the run kept outside git to the working copy; it ships a
   task where every method ties with the class prior, which adds only noise to the rankings.

   **Lennart (2026-10-21):** on the cross-dataset item "PROV-3 evidence standard": "either might be strong enough;
   on the columns we ship, and if the marks on the published file leak/extend to the shipped version (which is
   again case-by-case)".

   **Answer (AI, 2026-10-21):** the standard is set (PROV-3 and EV-3 amended): without a source statement or a
   generator, calibrated marks from two or more tests or marks linked to the label can each be enough, case by
   case, counted on the columns a definition would ship. Here the marks (no dependence HCV data must show, flat
   values, the stage unpredictable from any subset) were measured on all 28 features, which include the columns a
   definition at the biopsy would keep; they count when they hold on those columns (to confirm if it is kept).
   Still open: whether they are enough for `No` + `AHDS`.

2. **The record's "ALT features are future follow-up measurements, temporal leakage" (from an LLM) is half right.**
   The columns are measured during and after treatment, so a definition at the biopsy drops them, but they do not
   leak. With all 28 features the models stay at macro AUC 0.48-0.50.

3. **Where the file comes from is not settled.** The paper's 99.48% (abstract) cannot come from this file, so the UCI
   file is either a copy whose values were replaced column by column or a synthesised one; shuffled real values and
   replacement inside the codebook's bins are both ruled out (the run's evidence). The paper is closed access. To
   read it: Google "A novel model based on non invasive methods for prediction of liver fibrosis" pdf, or IEEE Xplore
   with DOI 10.1109/ICENCO.2017.8289800. The creators UCI lists (Sanaa Kamal, Mohamed ElEleimy, Doaa Hegazy, Mahmoud
   Nasr) could be asked for the real records; that would be the revisit condition.

5. **If the dataset is kept anyway (issue 1), two definition choices.** `AST 1` / `ALT 1` are labelled "1 week" in
   the UCI codebook (`ALT 1` also in the variable list), so strictly one week into treatment; they are kept as the
   first enzymes (alternative: drop them). The biopsy grade is dropped as a result of the same biopsy (alternative:
   keep it as a pathology co-variable, which changes the task to "stage given grade").

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap +, use case -, source -, shape -, risk - (Open issue 1: run recommends No (AHDS); independent columns suggest generated or replaced data). Likely generated or value-replaced file where every method ties with the class prior; would add only noise to rankings.

## Reference

A novel model based on non invasive methods for prediction of liver fibrosis
By Mahmoud Nasr, Khaled El-Bahnasy, M. Hamdy, S. Kamal. 2017

Published in International Computer Engineering Conference
