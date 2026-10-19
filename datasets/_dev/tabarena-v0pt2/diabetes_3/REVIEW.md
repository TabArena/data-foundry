# diabetes_3

**Outcome:** added. Efron et al.'s 442 patients from Hastie's LARS page, unstandardised and with the authors' column
names, as an IID regression of disease progression one year after baseline (RMSE). The AI recommends shipping it, with
the undocumented cohort as a concern (issue 1).

**Main points:** The cohort may not be diabetic (glucose at most 124). The `Trivial` marker is not supported.

**Record judgment:** valid with concerns: the data does not look like the paper's "442 diabetes patients", and no
source documents the clinic, the units or the response (issue 1).

**Issues for Lennart:**

1. **The cohort may not be diabetes patients, and nothing documents it (major; PROV-1 (criterion 4E) against your
   recorded acceptance).**
   - Evidence: the paper's only cohort fact is "442 diabetes patients" (Sec. 1, Table 1). Read as fasting plasma glucose
     in mg/dL, `glucose` runs from 58 to 124 (mean 91, a smooth distribution with no cutoff). No patient reaches the
     126 mg/dL threshold, 94 are in 100-125 and 348 below 100. Median BMI is 25.7 and median triglycerides 102 mg/dL,
     which looks like a general adult population.
   - No source gives the units, the clinic, the inclusion rule or how "a quantitative measure of disease progression
     one year after baseline" is computed. So we cannot check what y measures or whom a model would serve.
   - "Missing source information" does not apply: the file traces to the authors' page (2002) and the paper.
   - Implemented: kept, with an `Anomaly, cohort:` bullet in `curation_comments`.
   - Alternative: retire for lack of information (4E), or ask Efron/Hastie where the data and y come from.

2. **The `Trivial` marker is not supported.** The question is whether the record should drop it. By rule 4, one feature
   would have to match the methods fold by fold; it does so on 0 of 60 splits (R^2 0.30 against 0.49). The verifier's
   independent check (line, spline or LightGBM on the CV-chosen feature) stays below OLS, ridge and a random forest on
   60 of 60 splits, by at least 0.080. Methods spread, and the paper's least-squares fits reach an in-sample R^2 of
   about 0.50 (Sec. 3.4). Implemented: an ordinary tiny-data IID regression.

5. **The `sex` coding is undocumented.** Implemented: the codes 1 and 2 kept as categories (the 2002 file codes the
   same split 0/1). Code 1 has higher HDL (54.4 against 44.6 mg/dL) and lower blood pressure, which suggests
   1 = female. Alternative: label the codes female/male on that evidence (an inference, not a documented fact).

6. **The target is not logged.** The data check's distribution hint prefers lognormal (skew 0.44 raw, -0.33 logged;
   AIC 5221.9 lognormal against 5343.0 exponential). Implemented: raw scale, as the paper fits it by least squares.
   Alternative: `log_disease_progression_one_year`. The tail is short (25-346), so I see no need.
