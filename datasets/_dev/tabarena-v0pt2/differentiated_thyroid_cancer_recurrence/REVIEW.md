# differentiated_thyroid_cancer_recurrence

**Outcome:** added. UCI's 383 thyroidectomy patients from Hamadan as an IID binary task: recurrence during follow-up,
predicted at the initial staging (ROC AUC), without the response to therapy and the radiotherapy column. The AI
recommends shipping it; the label's definition is unverified (issue 2).

**Main points:** `Response` and `Hx Radiothreapy` dropped as after the prediction point; label definition unverified.

**Record judgment:** valid with concerns: `Response` is a near-copy of the outcome (dropped, issue 1), the radiotherapy
column is undefined (dropped, issue 6), and the paper's definition of recurrence could not be read (paywall, issue 2).

**Issues for Lennart:**

1. **`Response` (response to therapy) dropped: confirm the prediction point.** Evidence: the data creator's group says
   it "was determined based on the laboratory findings of thyroglobulin and antithyroglobulin and a whole-body scan"
   (Khazaei et al. 2024, Methods), i.e. a post-treatment assessment. Tuttle et al. 2010 (Thyroid 20:1341; cited by the
   source paper; abstract, Methods): ATA risk is assigned "as part of initial staging", and "Clinical data obtained
   during the first 2 years of follow-up (suppressed thyroglobulin [Tg], stimulated Tg, and imaging studies) were used
   to re-stage each patient based on response to initial therapy". ATA 2015 guidelines (Haugen et al. 2016, Thyroid
   26:1), section [B29]: "Structural incomplete response: persistent or newly identified loco-regional or distant
   metastases", which is the outcome. In the file 89 of 91 structural-incomplete patients recurred, 1 of 208 with an
   excellent response. ROC AUC (10 x 3 folds, raw file): `Response` alone 0.978; `Response` + `Risk` 0.989 (logistic),
   above all 16 columns (0.983-0.987); without `Response` 0.911-0.932. Implemented: dropped; the task predicts at
   initial staging. Alternatives: (a) keep `Response` as a "dynamic risk at the first response assessment" task:
   near-trivial (two features beat all) and flagged by the generated probe; (b) keep `Response` but only patients
   without structural disease at that assessment: 292 patients with 19 recurrences, about 6 per test fold, `Too Small`.
   Supporting inference (not verified): the file uses the 2015 ATA categories (Tuttle 2010 still used excellent /
   acceptable / incomplete), while every patient was diagnosed at least 10 years before the 2023 paper, so the
   categories were probably assigned from the records with the follow-up known.

2. **The definition of the label is not verified (paper paywalled).** `Recurred` seems to include persistent disease:
   all 18 M1 patients and all 32 ATA high-risk patients are labelled recurred (Tuttle 2010: "Persistent structural
   disease or recurrence" in 68% of high-risk patients), and 89 of 91 structural-incomplete responses. Khazaei et al. do
   not define recurrence either ("mainly local involvement"). The task stays valid either way: the ATA initial risk
   system estimates "the risk of persistent/recurrent disease" (ATA 2015, [B19]); this is now in the `Note:` bullet. The
   Springer page, its Wayback snapshot (2025-12-29) and Europe PMC (PMID 37902840) show only the abstract; ORBi UMONS
   and ORBi ULiège serve "Request a copy". Please get the PDF (Google: `"Machine learning for risk stratification of
   thyroid cancer patients: a 15-year cohort study" pdf`) and check how recurrence, the response and the radiotherapy
   column were defined and when each variable was recorded, and which 13 features the paper used.

3. **`Trivial` marker:** without `Response` the task does not meet rule 4's test for `Trivial`. On the 60 shipped splits
   `Risk` alone gives 0.896; logistic regression 0.929, random forest 0.929 and untuned CatBoost 0.932 beat it on 59, 59
   and 60 splits (CatBoost's mean gain 0.036, SE 0.002); the best two-feature lookup, `Risk` x `Gender`, gives 0.917 and
   is beaten by the best of the three methods on 54 of 60. No task-probe flags. The marker came from the paper's
   numbers, which probably include `Response` (issue 2). Proposal: remove the marker or note it as answered (record
   comment drafted).

4. **Duplicates kept.** 26 exact copies (22 profiles, 6.8%), all low-risk women who did not recur. Chance test:
   permuting `Age` within ATA risk x sex (2,000 draws) gives 23.2 duplicate feature vectors on average (95% range 17-30)
   against 27 observed (p = 0.16), so the copies are the repeats expected among distinct patients. 9.3% of test rows
   have a copy in train; dropping them from test lowers AUC by 0.002-0.003. Implemented: kept, warning accepted.
   Alternative: drop the copies (357 rows).

5. **`Stage` and `M` anomalies.** `Stage` follows AJCC 8th edition from `Age`, `T`, `N`, `M` in 371 of 383 rows; of the
   other 12, two match the 7th edition and ten match neither (e.g. age 26 with M1 recorded as stage I; 8th edition 371
   matches, 7th 279). 2 of the 18 M1 patients (ages 26 and 37) are ATA intermediate risk although distant metastases are
   ATA high risk (Tuttle et al. 2010, Table 1), so their M1 may have been found after the initial staging. Dropping `M`
   and `Stage` changes logistic-regression AUC by +0.001. Implemented: kept as recorded (`Anomaly:` bullet).
   Alternative: recompute the stage from AJCC 8th, or drop `M` and `Stage`.

6. **`Hx Radiothreapy` dropped (new after verification).** No source defines or dates it (UCI variable table empty;
   Khazaei et al. do not list radiotherapy among the collected variables). 6 of its 7 "Yes" rows are ATA high-risk male
   smokers, 5 with M1, 5 aged 61-81, all recurred; the seventh is a 25-year-old low-risk woman who did not. That fits
   external-beam or palliative radiotherapy for advanced disease (possibly after the prediction point), though an
   earlier head-and-neck radiotherapy (e.g. for another cancer in older smokers) fits too. On the 60 splits of the
   version that kept it, logistic regression scores 0.930 with and without it (random forest 0.928 and 0.929).
   Implemented: dropped. Alternative: keep it with a `Potential leak, kept on purpose:` bullet and revisit once the
   paper's variable definitions are read.
