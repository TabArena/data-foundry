---
unique_name: 2_month_survival_rate_prediction
name: 2 Month survival rate prediction
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 3
decision_markers:
- Outdated
tags:
- New IID
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Later'
- Dated Event Log
collections:
- New (BeyondArena)
original_source: Other
year: '2003'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
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

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes. For the curator (Review issues 5, 7, 8, 9): frame the use case as the source's objective estimate or keep the physicians' estimates and DNR; drop adlp, whose gaps hold 475 patients with interview status "Pt Death" (all positive, 0.0035 ROC AUC), against CC 2026-10-12; the year 2000 has no source (2001 or 2003); a pafi cut. Applied: prediction point named study day 3, alb above 6 g/dL set missing, wblc 0 noted, the split note and four inexact sentences corrected with the measured numbers. The earlier "no known risk" no longer holds. Priority 3: gap -, use case +, source +, shape +, risk - (adlp's gaps encode deaths after day 3, a confirmed leak open in issue 7).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — ROC area (C index) of the SUPPORT prognostic model for 2- and 6-month survival (Knaus et al. 1995, Ann Intern Med 122(3):191-203, The SUPPORT prognostic model).

CC (2026-10-26, Lennart): issue 7: drop adlp, "as recommended, that makes sense to me". This replaces the CC of 2026-10-12 for adlp: its gaps hold the 475 patients whose ICPSR interview status is "Pt Death", all of whom die within 2 months.

CC (2026-10-26, Lennart): issue 10: drop edu and income, "it is also better for fairness maybe". This replaces CC 2026-10-12 for edu and income: both come from the interview of days 2-7 and are missing more often among the deaths on days 4-7 (edu 31.4% against 16.3%, income 43.0% against 31.5%; LEAK-10).

CC (2026-10-26, Lennart): issue 9: set pafi above 713 missing, "this makes sense to me"; the values from 650 to 713 stay.

CC (2026-10-26, Lennart): issue 8: the year is 2003, the date of Vanderbilt's support2 extract (2003-06-23 inside hbiostat's zip), the first publication of the rows we ship (PROV-9). ICPSR 2957 V1 (January 2001) holds the study data in another form (race blanked, missing physiology filled with normal values, follow-up to 1997), so it does not hold every value we ship, and only places rows.

**Assessment (AI, 2026-10-26):** the marks of 2026-10-26 applied: adlp, edu and income dropped (22 features, all interview fields gone), pafi above 713 set missing (9 patients, 714-890, 4 of them deaths within 2 months), year 2003. `dataset check` clean; task probes: random forest ROC AUC 0.802 (0.806 before), linear 0.784, no flag. Issue 5 was settled later the same day (below).

CC (2026-10-26, Lennart): issue 5: "do (a)": the use case is SUPPORT's objective estimate of 2-month survival, set beside the physician's own estimate (Knaus et al. 1995, "Objective estimates of survival"; the physicians were interviewed on day 3 as the comparator). The physicians' estimates prg2m and prg6m and the DNR fields stay out by the use case. This differs from breast_cancer_prediction (BI-RADS kept, CC 2026-10-15), where the reading is the actor's own input.

CC (2026-10-26, Lennart): the declared metric, ROC AUC (the source's ROC area of the SUPPORT prognostic model), is checked as declared.

**Assessment (AI, 2026-10-26):** `use_case`, `changes`, the notes and the decision table now say why the physicians' estimates and DNR are not inputs; `dataset check` clean. No open issue is left in the folder's REVIEW.md, which is removed; the record keeps `WIP (DF)` until the curator's ship verdict.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `ca` (the README lists their levels).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `gossis_icu_hospital_mortality` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-19, Andrej): three half-year windows on the rebuilt entry date with a 60-day gap (Review issue 3, B): the order is rebuilt from file position within each block (survivors' Spearman 1.000 with their entry dates); Kumo-Tabular reads the relation flat, but where windows can be built the split is temporal.

## Review

**Outcome:** added. Reopened by the full-information split check of 2026-11-18: the shipped split disagreed with the split tree; the issue below holds the decision.

**Main points:** Split on the recovered entry date instead of random patients?

**Issues for Andrej:**

3. **Split on the recovered entry date instead of random patients?**

   * **Problem:**
     - The definition's own notes say each patient's entry date can be recovered (a survivor entered on 31 Dec 1994 minus `d.time`, and the rows of each of the file's ten blocks are in entry order, Spearman 1.000), while its time basis line says the file has no date.
     - Where an arrival order can be rebuilt the forced step rebuilds it and walks the tree again[^s22]; patients scored on study day 3 for a 60-day outcome then get windows on the entry date with a gap of about 60 days.
     - Without the rebuilt order the two study phases test flat, which makes the tag `StationaryRelation`; `ForcedIIDFromTemporal` fits neither path.
   * **Experiments:** from the definition's notes (review panel, 2026-10-20) and the stationary-relation test of 2026-11-18 (v2; the v3 re-run confirms flat).

     | Split | LightGBM ROC AUC |
     |---|---|
     | random, 9 splits | 0.818 |
     | three windows over phase II on the entry order | 0.824 |
     | phase I → phase II | 0.820 |
     | phase test: gap of the forward model (LightGBM; Kumo-Tabular) | +0.001 ± 0.008; +0.003 ± 0.002, floor 0.002: flat |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 3 x 3 random folds over patients, `ForcedIIDFromTemporal` (implemented) | No change | No rebuild | No leaf gives it |
     | B | Windows on the rebuilt entry date, a 60-day gap, `Time: Inferred` | The entry order orders the split and is no input | The tree's leaf; the source itself validated forward, phase I on phase II | The order is rebuilt within blocks (probably hospitals) and aligned through the survivors' dates |
     | C | The same random folds, `StationaryRelation` | The phase test goes into the Time basis line | No rebuild | Leaves an order the data holds unused |

   * **Recommendation:** B, because the data gives the order and the tree rebuilds it where it can. **Decision:** A, B or C?

   **Notes for the AI:** windows over the newest half per the window-count item; the gap = 60 days or training only on patients whose 60 days ended before the window; record facts `Time: Inferred`; a splits_comment naming the phase I → II validation.

   [^s22]: **SPLIT-36**, the tree's forced step: "can the sample arrival order be reconstructed from the data? ... Yes → rebuild it and walk the tree again from the root, with the order as recovered time (Time: Inferred)."

   **Answer (AI, 2026-11-18):** reassessed with the new forced step (the interchangeable question first; measured not flat leads to whole periods or Too Small) and the pooled flat verdict.

   - The reconstruction question still comes first, so B (windows on the rebuilt entry date) is the tree's answer.
   - If you decline the rebuild, the v3 test reads flat, so C (random, `StationaryRelation`) holds. Recommendation unchanged: B.

   **Andrej (2026-11-18, discuss):** You need to reassess stationarity with Kumo, LightGBM is not enough. Do that and then apply our rules to decide stationarity.

   **Answer (AI, 2026-11-18):** Kumo-Tabular measures the relation flat on every half-year of the rebuilt entry order, so the relation is stationary; under the rules the windows still come first, because the order can be rebuilt and gives three windows: B.

   - **Rebuilt order:** file position within each of the ten blocks, Spearman 1.000 with the survivors' entry dates; deaths placed between neighbouring survivors (median 2 days apart). Eight half-years, 934 to 1,284 patients each; patients entering in the 60 days before a test period are left out of its training.
   - **Kumo-Tabular:** no period is not flat. Pooled over the newest three periods the gap is +0.0002 ± 0.0011 ROC AUC, two SD 0.87 floors (flat); LightGBM +0.0024 ± 0.0030, 2.46 floors. Across the phase gap (1992H1) Kumo reads −0.0021 ± 0.0015. Phase I alone with its physiology columns is flat too.
   - **The rules:** the forced step asks first whether the order can be rebuilt (yes), then walks the tree again: three half-year windows (1992H2, 1993H1, 1993H2 with January 1994) train on 56%, 69% and 82% after the 60-day gap. SPLIT-32: "Where the windows can be built, the split is temporal however flat the relation"; the flat measurement goes in the notes as what the windows cost (about nothing). C (`StationaryRelation`) applies only where windows cannot be built.

   | Test period | Train / test | Kumo forward | Kumo contemporaneous | Kumo gap ± SD (floor) | LightGBM gap ± SD (floor) | Verdict |
   |---|---|---|---|---|---|---|
   | 1990H1 | 964 / 529 | 0.7614 | 0.7698 | +0.0084 ± 0.0102 (0.0027) | −0.0025 ± 0.0113 (0.0023) | flat |
   | 1990H2 | 2,041 / 477 | 0.7286 | 0.7323 | +0.0037 ± 0.0030 (0.0023) | +0.0046 ± 0.0077 (0.0020) | flat |
   | 1991H1 | 3,026 / 467 | 0.7357 | 0.7362 | +0.0005 ± 0.0034 (0.0024) | +0.0055 ± 0.0089 (0.0022) | flat |
   | 1992H1, across the phase gap | 4,232 / 586 | 0.7603 | 0.7583 | −0.0021 ± 0.0015 (0.0026) | +0.0000 ± 0.0073 (0.0023) | flat |
   | 1992H2 | 5,029 / 549 | 0.7479 | 0.7494 | +0.0016 ± 0.0018 (0.0025) | +0.0057 ± 0.0044 (0.0024) | flat |
   | 1993H1 | 6,179 / 623 | 0.7610 | 0.7602 | −0.0008 ± 0.0022 (0.0026) | +0.0009 ± 0.0071 (0.0025) | flat |
   | 1993H2 + Jan 1994 | 7,369 / 608 | 0.7463 | 0.7461 | −0.0002 ± 0.0016 (0.0025) | +0.0008 ± 0.0034 (0.0024) | flat |

   Gap = contemporaneous minus forward ROC AUC, 10 seeds; the repository's stationary-relation probe, unmodified; 11 non-physiology features (the files restoring phase II's physiology are not local).

   **Recommendation:** B, windows on the rebuilt entry date with a 60-day gap, `Time: Inferred`, the Kumo measurement in the notes. If you would rather take the flat measurement as the answer and keep random folds, that is C, which needs a departure from SPLIT-32. **Decision:** A, B or C?

   **Andrej (2026-11-19, discuss):** Agree.

   **Resolved (2026-11-19, Andrej):** B. Three half-year windows on the rebuilt entry date with a 60-day gap: 1993-07-01 to 1994-01-21 (1,216 patients, train 82.2%), 1993-01-01 to 1993-06-30 (1,247, 68.9%) and 1992-07-01 to 1992-12-30 (1,099, 56.1%); `entry_date` orders the split and is no input (`time_of="label"`); `ForcedIIDFromTemporal` and its `Time basis:` line are gone; the record's `required_split` reads Temporal; its facts keep `Time: Dated` (a Dated Event Log): the survivors' entry dates are exact (end of follow-up minus days followed), and the deaths are placed between them. The Kumo-Tabular measurement is in the notes as what the windows cost. Not rebuilt: the ICPSR files that restore phase II's physiology are not on this machine, so `dataset check` ran on a scratch copy (0 errors; `task_label_time_gap` and `splits_below_target` to accept with this decision).

   **Andrej (2026-11-19, discuss):** Agree.

   **Resolved (2026-11-19, Andrej):** B. Three half-year windows on the rebuilt entry date with a 60-day gap: 1993-07-01 to 1994-01-21 (1,216 patients, train 82.2%), 1993-01-01 to 1993-06-30 (1,247, 68.9%) and 1992-07-01 to 1992-12-30 (1,099, 56.1%); `entry_date` orders the split and is no input (`time_of="label"`); `ForcedIIDFromTemporal` and its `Time basis:` line are gone; the record's `required_split` reads Temporal; its facts keep `Time: Dated` (a Dated Event Log): the survivors' entry dates are exact (end of follow-up minus days followed), and the deaths are placed between them. The Kumo-Tabular measurement is in the notes as what the windows cost. Not rebuilt: the ICPSR files that restore phase II's physiology are not on this machine, so `dataset check` ran on a scratch copy (0 errors; `task_label_time_gap` and `splits_below_target` to accept with this decision).

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
