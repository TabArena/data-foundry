# stroke_prediction

**Outcome:** added; recommended `No` (`AHDS` or `Data Quality Issue`). Stroke (binary, IID) on the full training
file of the 2018 McKinsey Analytics hackathon (43,400 patients) instead of the record's Kaggle cut, with bmi dropped.
The AI recommends `No`: the file is partly generated or altered (issue 1). The folder stays until Lennart decides.

**Main points:** The file is partly generated or altered. bmi is dropped, because a missing BMI follows the stroke.

**Record fields that disagree with the definition:**

- `year`: record `2021`, definition `2018`.

**Record judgment:** valid with concerns, now leaning do not add (criterion 4B, partly generated data; issue 1).
Provenance is traced, but the data are partly generated or altered.

**Issues for Lennart:**

1. **The file is partly generated or altered. Recommendation: `No` + `AHDS` / `Data Quality Issue`**, retire the
   folder. The record accepted "might be fake ... use it for now and filter later if needed"; the evidence now says
   filter.
   - Residence_type, ever_married and work_type carry nothing beyond age. Likelihood-ratio tests with 1-year ages
     against all other columns give p = 0.47, 0.39 and 0.68-0.88 (test file 0.24-0.85); the sex column gives
     p = 7e-145.
   - LightGBM predicts each of them as well from age alone as from all columns, e.g. married 0.840 / 0.837. The same
     test on 35,850 BRFSS 2015 adults does find dependence: metro 0.505 -> 0.558, married 0.713 -> 0.761,
     self-employed 0.615 -> 0.694.
   - Married at 25-29: 45.0% of women and 45.0% of men (BRFSS: 53.8% / 40.3%). Work types are identical by sex
     (p 0.64-0.79).
   - Residence_type is a 50/50 coin, independent of everything (p 0.29-0.98).
   - Glucose has no value below 55.00, is flat at 55-64 and doubles at 65, in both contest files. 9.8% of patients
     have a post-meal glucose below 66 mg/dL.
   - The clinical columns look real (male x heart disease age-adjusted OR 2.28; BRFSS 1.87).
   - Precedents: churn and customer_satisfaction_in_airline were retired. The Analytics Vidhya siblings are held at
     2nd tier.
   - If kept: add `data_tags = ("2ndTierData",)` and drop the three columns. They add nothing: regularised LightGBM
     0.850 with and without them, per split -0.002 to +0.002.

2. **Version shipped: the contest's full training file, not the record's Kaggle cut** (8.5x the rows, 3.1x the
   strokes; 261 against 83 per test fold).
   - Alternative: the 5,110-row Kaggle file.

3. **bmi dropped as a leak: a missing BMI follows the stroke.**
   - With 1-year ages, sex, marriage, residence, hypertension, heart disease, glucose, smoking and work type fixed, a
     stroke multiplies the odds of a missing BMI by 3.69 (2.99-4.57). That is more than hypertension (2.50) or heart
     disease (2.19), and holds at 2.95-4.12 in every adult age band.
   - Smoking-status missingness does not follow the stroke (OR 0.96, 0.80-1.16).
   - BMI values add nothing beyond the missingness: 0.861 as is, 0.847 without the column, 0.846 with missing values
     drawn at random.
   - Alternative: keep bmi with a "Potential leak, kept on purpose" bullet (+0.014 AUC).

4. **Age dominates.** Without bmi, the strong models beat raw age (0.840) on 9 of 9 splits, but only by 0.010. Not
   `Trivial` by rule 4, as in the sepsis_survival precedent. With three noise columns, the signal beyond age comes
   from sex, hypertension, heart disease, glucose and smoking. This adds to issue 1.

5. **Cross-sectional label.** The features may postdate the stroke; the file has no dates. Documented in the
   prediction-point bullet (as cdc_diabetes_health_indicators does).

6. **Anomalies kept.**
   - Ages under 2 are written as years plus 0.08 per month (0.08-0.88, 1.0-1.88).
   - Ages 78-82 are over-full (435-698 per year against 336-446 at 70-77), as if older ages had been folded in.
   - There are strokes at ages 1.32 and 14.
