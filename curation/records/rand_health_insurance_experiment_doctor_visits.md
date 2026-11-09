---
unique_name: rand_health_insurance_experiment_doctor_visits
name: RAND Health Insurance Experiment next-year medical spending (statsmodels randhie / Cameron & Trivedi extract), 1974-1982
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target / Scientific Discovery
- Outdated
tags:
- Two-Regime Zeros
- Non-IID (Grouped)
original_source: Other
year: '1995'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.statsmodels.org/dev/datasets/generated/randhie.html
- http://cameron.econ.ucdavis.edu/mmabook/mmadata.html
- https://doi.org/10.3886/ICPSR06439.v1
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: the earlier `No` (a discovery table) is no fast reject,
since the HIE data was used to predict annual spending for capitation rates (Newhouse et al. 1989); it stays secondary
because the data is 40-50 years old and `meps_total_healthcare_expenditure` carries the same task today.
- Source: the RAND Health Insurance Experiment (1974-1982, six US sites), ICPSR 6439: "The main purpose of the
  experiment was to assess how the cost of health services affected individuals' use of services" (earlier AI triage).
  The extract is Cameron and Trivedi's `randdata.dta` ("Authors' extract", the count-data example citing Deb and Trivedi
  2002, J. Health Econ.; their data page); statsmodels `randhie`: 20,190 observations, 10 variables, "This is in the
  public domain". 5,912 persons, `mdvis` 0 for 31.2%, `meddol` 0 for 22.1% (earlier AI triage).
- Use case: Newhouse, Manning, Keeler and Sloss 1989 (Health Care Financing Review 10(3):41-54, PMC4192960), Methods,
  "Source of data": "The data we use come from the RAND Health Insurance Experiment"; "Dependent variables": "to
  estimate or predict annual expenditures for medical care services in constant dollars", framed by Medicare's payment
  to HMOs per enrollee (Introduction). So a payer sets next year's capitation from health measures and prior use; fit
  approximate (enrollees of an experiment under randomised plans, 1970s care). Regime grouped by person (`zper`), or a
  next-year framing with the previous year's use as a feature (USE-10).
- Siblings and duplicates: `meps_total_healthcare_expenditure` (Yes, Andrej) is the same kind of task on other data, not
  a duplicate (PROV-7); `health_insurance` (No, an econometrics table of the 1993 CPS) is another source. External
  collections: statsmodels' `randhie` only.
- Papers and pages: Newhouse et al. 1989; Deb and Trivedi 2002 (latent class against two-part models of the visits);
  Cameron and Trivedi 2005.
- Metric: none deliberate found (Newhouse et al. give shares of explained variance in the abstract, their text read for
  the data and the purpose only; Deb and Trivedi 2002 not read), so the fallback `rmse`; inputs none.
- Risks for /add-dataset: the same-year utilisation and spending columns are outcomes (LEAK-10; the 12 named in the note
  below); the plan variables are the experiment's treatment, which no payer assigns; the target to pick (visits or
  spending, same or next year); `No Good Target / Scientific Discovery` and `Outdated` kept as the open concerns. No
  open family question applies (a zero is an observed year without use).
- Priority: gap 0 (medical, the largest domain), use case 0 (named by a later paper, fit approximate), source + (ICPSR
  and the authors' extract), shape + (5,912 persons over 3-5 years), risk - (outdated, outcome columns to drop).

CC (2026-10-30, Andrej): `Yes`, priority 2 (the AI screening had `TBD -> 2nd Tier`, priority 2; zero-inflated screening
review page). "Try to find a target and if not we can still reject it"

Person-year extract of the RAND Health Insurance Experiment (1974-1982, six US sites) from Cameron and Trivedi's
Microeconometrics data page (randdata.dta, 20,190 rows x 45 columns); statsmodels' `randhie` keeps the visit count and
9 of the covariates. ICPSR 6439: "The main purpose of the experiment was to assess how the cost of health services
affected individuals' use of services, their satisfaction with health care, the quality of their care, and the state
of their health." The covariates are the randomised plan (coinsurance, deductible, participation incentive,
maximum-expenditure offer) plus baseline demographics and health, so a visit model is the demand equation behind a
price-elasticity estimate, on data now 50 years old. Same call as `health_insurance` (an econometrics study of the
1993 CPS).

Measured: 5,912 persons (most with 3 or 5 years); `mdvis` has 31.2% zeros (max 77), medical spending `meddol` 22.1%.
The 9 statsmodels covariates are constant within a person and take only 2,760 distinct vectors over 20,190 rows,
so a split must group by person (`zper`, in the extract only). Untuned LightGBM grouped by person:
AUC 0.69 for any visit and R^2 0.02 on log1p visits among users with the 9 columns; 0.75 and 0.08 with the 30 columns
that are not utilisation or spending; 0.79 and 0.27 with the previous year's visits and spending added. The same-year utilisation and
spending columns (`meddol`, `outpdol`, `drugdol`, `suppdol`, `mentdol`, `inpdol`, `totadm`, `inpmis`, `mentvis`,
`notmdvis`, `lnmeddol`, `binexp`) are outcomes. The ICPSR public-use files add expenditure and health detail but no
other purpose; `meps_total_healthcare_expenditure` is the current version of this task. statsmodels: "This is in the
public domain"; ICPSR lists no access restriction for 6439.

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/rand_health_insurance_experiment_doctor_visits/` by /add-dataset with the full review panel; the open questions are in its Review. Recommend shipping; only the forced split (its issue 1, against your how_much_did_it_rain call) can turn it to `No`. The target is next-year `meddol` in dollars (Newhouse et al. 1989), scored by `r2`; the split is grouped by the rebuilt family and tagged `ForcedGroupedFromTemporal`; under the next-year framing the year-t use columns are history, not outcomes. This supersedes the screening's "Metric: ... fallback `rmse`" line, its risk line on outcome columns and the "Same call as `health_insurance`" paragraph above. The title now says spending (the folder keeps its name, issue 3). The marker `No Good Target / Scientific Discovery` stays until your mark. Priority 2: gap 0, use case 0 (fit approximate), source +, shape +, risk - (issue 1).

CC (2026-11-02, Andrej): the forced grouped split ships (issue 1 (a)): "Forced group splits should be fine. Regarding forced IID, did you make sure there are no leaks? Whenever there are no leaks we can ship." Recorded in SPLIT-8 (amended 2026-11-02: a forced grouped split ships; a forced IID split ships only when the leak test across the random split finds none).

**Assessment (AI, 2026-11-02):** the leak test across the forced grouped split (3x3 family folds) finds none. Shared rows: no feature row recurs across the split; a person-level key (the baseline values and the birth cohort, age minus study year) links 0.2% of test rows to a training row, and those rows' spending tracks the test target at correlation 0.04; the hidden-group probe finds no group; neighbouring families in person-id order are no more alike than random pairs (residual correlation 0.014 against 0.000 +- 0.022). Shared period: adding the training side's mean target of the test row's site and study year (leave-own-family-out on the training side) changes R2 by -0.004 (LightGBM, SE 0.002) and +0.000 (ridge), a placebo cell mean by -0.000; the study-year mean alone by -0.011 and -0.002. Features from other rows' outcomes: none (column audit: every feature is the row's own year t or its enrolment baseline; `family_income`, the one open timing, is dropped). how_much_did_it_rain's `No` named a measured shared-period leak; none is found here.

CC (2026-11-03, Andrej): 2nd Tier: "The target is a bit made up and the data is quite outdated. Could generally be considered, but currently there are better options". The v2 folder left the working copy; its last definition is in the run folder of 2026-11-03, the committed one in 902011b3.

CC (2026-11-03, Andrej): issues 2 and 3: "We don't ship"; moot with the dataset out (`TBD -> 2nd Tier` stays).

## Reference

Newhouse J.P. RAND Health Insurance Experiment [in Metropolitan and Non-Metropolitan Areas of the United States],
1974-1982. ICPSR 6439, version 2005-11-04. doi:10.3886/ICPSR06439.v1. Extract: Cameron A.C., Trivedi P.K. (2005).
Microeconometrics: Methods and Applications. Cambridge University Press; data randdata.dta at
http://cameron.econ.ucdavis.edu/mmabook/mmadata.html.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
