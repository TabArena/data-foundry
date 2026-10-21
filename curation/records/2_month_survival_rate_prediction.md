---
unique_name: 2_month_survival_rate_prediction
name: 2 Month survival rate prediction
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
decision_markers:
- Outdated
tags:
- New IID
collections:
- New (BeyondArena)
original_source: Other
year: '2000'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/880/support2
- https://doi.org/10.3886/ICPSR02957.v2
- https://hbiostat.org/data/
- https://hbiostat.org/data/repo/supportdesc
v2_path: datasets/_dev/tabarena-v0pt2/2_month_survival_rate_prediction/dataset.py
source_row: 687
type_adapter_id: curation-record-v1
---

## Comments

Multi-target task?

Need to filter predictions from features, need to determine best target (binary or regression), need to filter dnr

**Assessment (AI, 2026-10-07):** In support2.csv (and UCI 880) the 14 day-3 physiology columns of most phase II patients belong to another patient, up to 87 rows away. crea against aps (APACHE III score of the same values) has Spearman 0.52 in phase I and 0.05 in phase II; in rows 4,351-5,700 it is 0.54 against the row 47 lines down. Added with phase I only (the five file blocks without bun, glucose and urine, 4,301 patients): 4,232 alive after day 3, target death before day 60 (34.2%), 27 features, LightGBM ROC AUC 0.80. Dropped as supportdesc advises: sps, surv2m, surv6m, aps, prg2m, prg6m, dnr, dnrday; also outcomes, costs and avtisst. Alternative: re-source the physiology from ICPSR 2957.

**Assessment (AI, 2026-10-12), ICPSR 2957 and the restored physiology:** The study's own data (ICPSR 2957 V2, public-use parts 9 and 10, downloaded by Lennart on 2026-10-12) settle the phase II problem, and the definition now uses both phases (8,967 patients alive after day 3, 33.4% positive).
- Data used, and from where: every value of the dataset comes from hbiostat's support2.csv. From ICPSR we read ten link columns of part 10 and the day-3 physiology of part 9; they only decide which row of support2.csv each patient's physiology is taken from. The build reads the ICPSR files from `local-data-warehouse/2_month_survival_rate_prediction/icpsr_2957/` (login download, steps and SHA-256 in `download_description`); nothing from ICPSR is in git.
- Link: support2 has no patient id. Each row matches exactly one ICPSR patient (`pseudoid`) on length of stay, hospital death, days in hospital before entry, number of comorbidities, age in whole years, disease group, sex, sps, scoma and aps (all 9,105 rows). The outcomes, not used for the link, agree: all 6,201 support2 deaths have the same day of death in ICPSR; ICPSR follows survivors to 1997 instead of the end of 1994, and 878 of them died later, the earliest on day 361, so the 2-month target is the same in both.
- Locate: each patient's ICPSR day-3 values, with ICPSR's normal-value fills set missing as support2 has them (codebook Appendix B), are looked up among the physiology blocks of support2.csv. Every patient's block is in the file exactly once. Phase I rows hold their own (4,301 of 4,301; the rule reproduces support2's phase I values and missing values exactly); 431 of 4,804 phase II rows do, and for the others the block sits 1 to 90 rows further down, with jumps at block ends. All 14 block columns (meanbp to urine) move together; every other column is on its own row (ICPSR confirms 21 of them on every row; edu, income and race are blanked in ICPSR and could not be checked).
- Restored, phase II behaves as phase I: Spearman with aps for crea 0.49 (phase I 0.52, published 0.05); each column's ROC AUC alone 0.50-0.64 (published 0.50-0.53). LightGBM fit on phase I scores ROC AUC 0.812 on phase II restored, 0.695 as published.
- Also changed with the new cohort: bun, glucose and urine stay dropped (not measured in phase I). adls and adlsc are dropped (Lennart, below): the ADL answers describe function two weeks before admission, but the interviews took place on study days 2-7 (median day 4), adls is missing for 46% of the patients whose stay ended by day 7 against 24% of longer stays, and adlsc's imputed values used the interview status, whose groups include "Pt Death" and "Pt Discharged" (codebook Appendix A). adlp, edu and income stay: adlp is missing mostly when the patient cannot answer, and edu and income are missing as often for short as for long stays. 25 features. Probes (2026-10-12): random forest ROC AUC 0.806, no task, leak, generated-data or hidden-group flag.
- Terms of use (noted): ICPSR's terms forbid redistributing its data or other materials without ICPSR's written agreement and ask to cite the study (second BibTeX entry).

CC (2026-10-12, Lennart): Use ICPSR 2957 only to put the phase II physiology back into the right rows, and ship only support2.csv's values.

CC (2026-10-12, Lennart): One target, death within 2 months; not a multi-target task (the 6-month and in-hospital framings are nested versions of the same signal).

CC (2026-10-12, Lennart): Drop adls and adlsc, keep adlp, edu and income: the surrogate interview's gaps depend on whether the stay lasted until the interview, which is after the prediction point.

**Assessment (AI, 2026-10-20):** priority 4 for the review of the added dataset: gap -, use case +, source +, shape +, no known risk. Well-documented clinical prognosis task whose misplaced phase II physiology was repaired from ICPSR; open issues only confirm cohort and drop choices.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes. For the curator (REVIEW.md issues 5, 7, 8, 9): frame the use case as the source's objective estimate or keep the physicians' estimates and DNR; drop adlp, whose gaps hold 475 patients with interview status "Pt Death" (all positive, 0.0035 ROC AUC), against CC 2026-10-12; the year 2000 has no source (2001 or 2003); a pafi cut. Applied: prediction point named study day 3, alb above 6 g/dL set missing, wblc 0 noted, the split note and four inexact sentences corrected with the measured numbers. The earlier "no known risk" no longer holds. Priority 3: gap -, use case +, source +, shape +, risk - (adlp's gaps encode deaths after day 3, a confirmed leak open in issue 7).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — ROC area (C index) of the SUPPORT prognostic model for 2- and 6-month survival (Knaus et al. 1995, Ann Intern Med 122(3):191-203, The SUPPORT prognostic model).

## Reference

@article{knaus1995support,
  title={The SUPPORT prognostic model: Objective estimates of survival for seriously ill hospitalized adults},
  author={Knaus, William A and Harrell, Frank E and Lynn, Joanne and Goldman, Lee and Phillips, Russell S and Connors, Alfred F and Dawson, Neal V and Fulkerson, William J and Califf, Robert M and Desbiens, Norman and others},
  journal={Annals of internal medicine},
  volume={122},
  number={3},
  pages={191--203},
  year={1995},
  publisher={American College of Physicians}
}
