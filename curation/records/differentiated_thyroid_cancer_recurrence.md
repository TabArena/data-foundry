---
unique_name: differentiated_thyroid_cancer_recurrence
name: Differentiated Thyroid Cancer Recurrence
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 1
tags:
- Tiny Data
collections:
- TabSTAR
original_source: UCI
year: '2023'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5632J
- https://www.openml.org/search?type=data&id=46605&sort=runs&status=active
v2_path: datasets/_dev/tabarena-v0pt2/differentiated_thyroid_cancer_recurrence/dataset.py
source_row: 788
type_adapter_id: curation-record-v1
---

## Comments

Might be panel / longitudinal data, but is already made to be IID

Otherwise, looks reasonable and might be a valid task

Performance in paper is already very high, likely trivial

**Assessment (AI, 2026-10-07):** One row per patient: the 383 differentiated cancers of a 400-patient endocrine-clinic cohort in Hamadan, 2008-2023 (Khazaei et al. 2024, J Res Health Sci 24:e00632, open access; Table 2 matches the file). `Response` is a post-treatment assessment ("determined based on the laboratory findings of thyroglobulin and antithyroglobulin and a whole-body scan", same paper, Methods), and a structural incomplete response is persistent or new metastatic disease (ATA 2015, [B29]): 89 of 91 such patients recurred. The v2 definition drops it and the undefined radiotherapy column and predicts at initial staging. ROC AUC is then 0.93 against 0.896 for the ATA risk alone (beaten on 59-60 of 60 splits), so `Trivial` does not hold. No open text defines recurrence.

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source +, shape -, risk - (Issue 2: label definition unverified, 'Recurred' may include persistent disease (paper paywalled)). Tiny clinical cohort (383 patients) predicting recurrence at staging; beats ATA risk alone, but the label definition is unverified.

**Assessment (AI, 2026-10-20):** Review panel (re-check): ship after changes, made in the definition. The fit is approximate: `M` is kept although 2 of the 18 M1 patients are ATA intermediate risk (a potential leak kept on purpose, +0.001 ROC AUC), the label's breadth is unverified and the data come from one clinic. `Risk` gets a potential-leak note (a crude ATA rule agrees in 337 of 383 rows; at most +0.010 ROC AUC), the use case names the decisions taken at staging (radioiodine, the TSH target, the initial follow-up schedule), and the follow-up is written as the source's claim, which conflicts with the 2008-2023 cohort period. Recurrence is 4.8% / 62.7% / 100% by ATA risk class against about 3% / 21% / 68% in Tuttle 2010, so the label probably counts persistent disease; all 34 high-risk or M1 patients recurred (ROC AUC 0.928 with them, 0.901 without, as for any equally easy positives). `Trivial` is refuted (TP-4: a random forest beats `Risk` alone, 0.896, on 59 of 60 splits). Open for Lennart (REVIEW.md): the label and the paper's cohort from the PDF (issue 2), drop or keep `Hx Radiothreapy` (issue 6), and two rule questions in the Across datasets view (USE-8 and an unverified label; thyroid_discordant's `Trivial`). Priority 1: gap -, use case - (the fit is approximate), source +, shape - (383 patients), risk - (the label's definition and the cohort are unverified).

CC (2026-10-21, Lennart): an unverified label definition makes the fit approximate ("yea it does"), and a potential leak kept on purpose does not by itself ("stay with direct fit if the task (without leakage) would be a direct fit"); USE-8 amended. The fit stays approximate, now for the unverified label (breadth and follow-up); the kept `M` is no longer a reason for it.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Borzooei et al. 2023 report AUC, sensitivity and specificity, none named as the criterion.

CC (2026-10-26, Lennart): the `Trivial` marker is removed, as the definition has it (TP-4: without `Response`, a random forest beats the risk class alone on 59 of 60 splits, mean gain 0.032 ROC AUC; the paper's 0.98-0.997 used `Response`).

**Assessment (AI, 2026-10-26):** the paper read (Borzooei et al. 2024, Eur Arch Otorhinolaryngol 281:2095-2104, the curator's PDF). Cohort: 383 patients of one centre, Table 1 with ATA high risk 32 and M1 18 as in the file, so the 34 high-risk or M1 patients are in the paper's cohort (issue 2: keep, (a)). Label: "recurrence status (including both locoregional and distant metastasis)", persistence not separated from recurrence. Follow-up: "a minimum follow-up period of 10 years ... The study spanned a period of 15 years". `Hx Radiothreapy` is "history of radiation therapy to the head and neck region", recorded with age and smoking at diagnosis (issue 6: keep, (b)). The paper's top feature is the structurally incomplete response (importance 0.843), which we drop.

CC (2026-10-26, Lennart): issue 2: "ok keep then": the 34 ATA high-risk or M1 patients stay, as the paper's cohort includes them (LEAK-22).

CC (2026-10-26, Lennart): issue 6, option (b): `Hx Radiothreapy` stays as a plain input, as the paper defines it as a history of head and neck irradiation collected at diagnosis ("ok (b)").

**Assessment (AI, 2026-10-26):** issues 2 and 6 applied: `Hx Radiothreapy` is back among the 15 features with the paper's definition in the notes; the label, cohort and follow-up notes quote the paper; the metric note cites its Table 2. dataset check: 0 errors, 0 warnings. No open issue left.

CC (2026-10-26, Lennart): verdict ship.

## Reference

@article{borzooei2024machine,
  title={Machine learning for risk stratification of thyroid cancer patients: a 15-year cohort study},
  author={Borzooei, Shiva and Briganti, Giovanni and Golparian, Mitra and Lechien, Jerome R and Tarokhian, Aidin},
  journal={European Archives of Oto-Rhino-Laryngology},
  volume={281},
  number={4},
  pages={2095--2104},
  year={2024},
  publisher={Springer}
}
