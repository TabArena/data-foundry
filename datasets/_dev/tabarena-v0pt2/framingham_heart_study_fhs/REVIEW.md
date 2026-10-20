# framingham_heart_study_fhs

**Outcome:** added. A binary task on the baseline exam of the NHLBI BioLINCC Framingham teaching dataset: a first
CHD event (ANYCHD) within 10 years, IID. The label is rebuilt from the event columns, because MIT's `TenYearCHD`
counts 265 non-CHD events among its 644 positives. The AI recommends shipping it, with the anonymized teaching data
as the open concern.

**Main points:** The label is rebuilt: the MIT/Kaggle `TenYearCHD` counts 265 non-CHD events among its 644
positives. Competing deaths count as No.

**Record fields that disagree with the definition:**

- `year`: record `2013`, definition `2004`.

**Record judgment:** valid with concerns: the defective label of the Kaggle/MIT file (issue 1) and the teaching
data's anonymization and terms (issue 3). All three Kaggle uploads are MIT's cut of the BioLINCC teaching dataset.

**Issues for Lennart:**

1. **Target: the Kaggle/MIT `TenYearCHD` is wrong for 265 of its 644 positives, and the endpoint is a choice.**
   - Evidence: `TenYearCHD` equals `TIMECHD < 3,652 days` in 4,240 of 4,240 rows (any cut-off from 3,647 to 3,654 gives
     the same). "Had a CHD event within 10 years" matches only 3,975 rows. TIMECHD is the day of the first CHD event
     or, without one, the "censor date ... end of followup, death or last known contact date if subject is lost to
     followup" (BioLINCC documentation 2021a, p. 4).
   - So 249 participants who died of other causes and 16 lost to follow-up within 10 years are positives. Only 379
     positives had a CHD event.
   - Implemented: the label rebuilt from ANYCHD/TIMECHD of the teaching data (4,224 rows, 379 Yes). Quick 3 x 3-fold
     ROC AUC (LightGBM / logistic regression): 0.699 / 0.739 on ours, against 0.692 / 0.723 on MIT's label.
   - Alternative: ship MIT's file and label as published (4,240 rows, 644 positives). I advise against it: 41% of its
     positives are not CHD. The same defect is in every paper or notebook that uses this Kaggle file.
   - Endpoint, your call:
     - ANYCHD (implemented): angina, MI, coronary insufficiency or fatal CHD. 379 Yes; the CHD of MIT's task.
     - Hard CHD (MI_FCHD: hospitalized MI or fatal CHD): the endpoint of the FHS hard-CHD 10-year risk page that the
       record links. 191 Yes (about 64 per test fold), 0.741-0.749 / 0.783-0.788.

2. **Competing deaths are No (the verifier agrees).**
   - Implemented: the 251 participants who died without CHD within 10 years are No, also those who died early (32
     within 2 years, 99 within 5, median day 2,193). This is the cumulative-incidence label.
   - Alternative: drop them, like the censoring of the Framingham risk functions: 3,973 rows, 379 Yes.
   - Against it: dropping them selects the cohort on an event after the prediction point and removes high-risk
     negatives. Their mean age is 54.8 against 54.1 for the CHD cases and 48.8 for the CHD-free; mean systolic BP 143.5
     against 144.0 and 130.3. Logistic regression rises from 0.737-0.739 to 0.751-0.754 (three seeds) only because
     these hard negatives go.

3. **The teaching data is anonymized, and BioLINCC calls it unsuitable for publication.**
   - BioLINCC teaching page: "teaching datasets are completely unsuitable for publication purposes since specific
     statistical measures were used to create anonymous versions". Documentation p. 1: "specific methods were employed
     to ensure an anonymous dataset ... this dataset is inappropriate for publication purposes".
   - What was changed is undocumented. Nahhas, *Introduction to Regression Methods for Public Health Using R*,
     App. A.6, names "permutations and/or random visit selection".
   - The riskCommunicator man page (the copy we read) states NHLBI's permission and omits the caveat. BioLINCC's
     teaching-request terms are behind a login; neither the verifier nor I read them.
   - The terms are noted, not a reason. The data-quality part is a real question: results on this task measure methods
     on perturbed data, and a benchmark publishes those results.
   - No visible damage:
     - systolic and diastolic BP correlate at r 0.78 at baseline;
     - within a person, BMI and systolic BP 6 years apart correlate at r 0.90 and 0.71; values permuted across
       participants at one exam would weaken this;
     - ages match the exam days in 3,930 of 3,930 period-2 and 3,263 of 3,263 period-3 exams;
     - HDL + LDL never exceeds total cholesterol (3,026 exams); the event logic is consistent;
     - 3 of 4,434 participants (all in the cohort, No either way) have a CHD censor date after their death.
   - Implemented: added, with these numbers in the Anomaly bullet and the terms in `license`.
   - Options:
     - tag `2ndTierData` ("not of the highest quality but still a reasonable task"; not applied: no defect found, and it
       is your quality call);
     - do not ship. The real FHS data needs a BioLINCC research application and cannot be redistributed.

5. **Raw-data route.**
   - CRAN ships an `.rda`, so `download_description` has a conversion step (`uvx` pyreadr, or `write.csv` in R).
     The Kaggle CSV shreyjain601 is an identical alternative if a plain download is preferred.
   - The MIT file is read only for the evidence table. If you prefer fewer raw files, drop it and keep the numbers in
     the comments.

6. **SelectArena: the same defect, and a wrong domain.**
   - `datasets/_dev/feature_selection/framingham_heart_study/framingham_heart_study.ipynb` builds a container from the
     aasheesh200 file with MIT's `TenYearCHD`, so it carries the defect of issue 1.
   - It also sets `domain_str="physics & astronomy"` (the verifier confirmed both).
   - For awareness; not touched.
