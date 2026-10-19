# corporate_credit_rating_cat_data_set_ratings_raitings

**Outcome:** added. The book's original `ratings.csv` (197 rated banks, six ratios), not the generated OpenML 46372,
as an IID regression on the rating code from 1 (AAA) to 10, scored with RMSE. The AI recommends shipping it, with the
provenance gaps of issue 3.

**Main points:** The book's 197 rows as a regression on the rating notch. OpenML 46372 is generated from them.

**Record fields that disagree with the definition:**

- `problem_type`: record `Multiclass Classification`, definition `Regression`.

**Record judgment:** valid with concerns: the data page names no agency, years or country, and gives the scale only
as "1 = AAA"; the record's first link, OpenML 46372, is generated from the 197 rows (issue 1).

**Issues for Lennart:**

1. **OpenML 46372 is generated.** The record's first link and TabSTAR's copy should not be used.
   - The evidence:
     - Its 5,000 rows (500 per code) draw every ratio independently and uniformly between the minimum and the maximum
       of the book's rows with the same code. All 30,000 values lie inside those ranges.
     - The class means sit at the range midpoints (within 3% of the range).
     - 57 of 60 code-ratio cells pass a KS test against that uniform (p > 0.05; the other 3 have p 0.031-0.039).
     - Within-code correlations between the ratios fall from mean |rho| 0.21-0.42 to 0.03-0.04.
     - No row is a book row. The ids look random: 4 of its 4,969 match a book id.
   - The verifier added three facts:
     - A KS test against the book's own rows of the same code rejects in 33 of 60 cells, so the rows were not
       resampled from them.
     - SIZE has 6 decimals in 4,547 of 5,000 rows, against 4 decimals in 182 of 197 book rows.
     - The Medium article never says the rows were generated.
   - The boxes make the classes separable: LightGBM reaches a 10-class macro ROC AUC of 0.974 on that file, against
     0.66-0.67 for logistic regression and a random forest on the book's rows.
   - OpenML also labels the codes 1 = "very_bad" to 10 = "outstanding", the reverse of the book's "1 = AAA".
   - Implemented: the book's file.
   - The record could get the book's file link as its first source, and a note that the TabSTAR / OpenML version is
     simulated.

2. **Target framing: regression on the notch (implemented) or classification (the record's leaning, "likely
   classification").**
   - Regression is the only framing with neither a Too Small class nor an assumed mapping.
   - Implemented: regression.
     - The R Companion's chapter 8 code scores the ordinal model in notches.
     - The codes move with the ratios as a 1 = AAA scale should: Spearman with size -0.50, liquid assets -0.39,
       equity +0.26 (small banks hold more equity), loan-loss provisions +0.20, ROE -0.17, costs to income +0.10.
     - Ridge R² 0.286 on the shipped splits; RMSE 1.57 against 1.88 for the mean. Per the verifier, ridge beats a
       random forest on 75% of the splits (paired SE 0.012).
     - Each test fold scores 65-66 institutions; a 161-row regression already ships.
     - Codes 1, 2 and 10 hold 1-7 test rows per fold (median 4): 6% of the test rows, but 29% of ridge's squared
       error.
     - The R code reports absolute notch differences; I kept RMSE, the collection's default (and the TabArena
       adapter's only regression metric).
   - Alternatives (logistic regression, 3-fold x 10 repeats, log loss against the class-prior baseline):
     - (a) 10 classes as shipped: 1.888 against 2.023, macro AUC 0.669. Codes 1, 2 and 10 hold 3, 5 and 4 rows, so
       the rarest class has 1 row per test fold: Too Small. The precedents drop classes under 10 rows
       (ecoli_proteins, lung_cancer).
     - (b) Drop codes 1, 2 and 10: 185 rows, 7 classes. 1.678 against 1.837, macro AUC 0.716. This drops the ends of
       the scale and still leaves codes 3 and 9 at 4 rows per test fold, near the parkinsons line.
     - (c) Letter grades under a notch reading, 1-4 (AA- or better) / 5-7 (A) / 8-10 (BBB): 54/109/34 rows, 11 of
       the smallest per fold. 0.830 against 0.986, macro AUC 0.762. This depends on an unverified mapping of the
       codes: only "1 = AAA" is given.

3. **Provenance gaps (cannot verify without the book).**
   - The data page names no agency, years, country or selection.
   - The book text was not read. The use case and the notch meaning come from the R Companion code transcription and
     Crossref.
   - The data favour notches over letter grades. Read as letters (AAA, AA, A, BBB, BB, B, CCC, CC, C, D), the 57
     institutions with codes 7-10 would be rated CCC or worse, while codes 7, 8 and 9 have median ROE of 11%, 8% and
     10%.
   - The two `spid` ranges (100,079-130,277 for 130 rows, 300,021-453,328 for 67) may mark two populations
     (regions, id systems or agencies).
     - They carry a little code information: mean code 6.24 against 5.36 (Mann-Whitney p 0.001); ridge residuals
       +0.36 against -0.19 (p 0.06).
     - A range flag lifts ridge R² from 0.286 to 0.299 on the 60 splits.
     - Kept dropped: no source says what the ranges are.
   - The file is two blocks of 98 and 99 rows, each sorted by rating, with no institution in both. A random forest
     separates the blocks at ROC AUC 0.52, so they may be estimation and validation halves, or two years.
   - The same book's HMEQ data was retired for generation artefacts, and its LGD data is "slightly modified and
     anonymized". The 197 rating rows pass the checks that caught HMEQ (near-copies, formats by class; the
     verifier's nearest-neighbour distance does not predict the code, R² -0.12) and have real within-code
     dependence.
   - Chapter 8 (pp. 213-236), if we can get the book, would settle four things: the scale (is 10 = BBB-?), the
     agency, period and sample, whether the data were modified, and what the id ranges are.
   - Implemented: kept, with `Note` / `Anomaly` bullets.

4. **Name.**
   - The `unique_name` carries TabSTAR's label of the generated file: the "raitings" typo, "cat", and "corporate" for
     what are bank ratios (loan-loss provisions to loans, liquid assets to total assets).
   - Implemented: the record's `unique_name`, as the brief requires.
   - Alternative: rename the record and the folder (for example `credit_risk_analytics_bank_ratings`) before the
     first build, while it is cheap. The verifier agrees.

5. **Licence note (not a verdict reason).**
   - The download form allows use "only in conjunction with the Credit Risk Analytics textbooks" and prohibits
     commercial use.
   - The site's terms.html says "You must not: Republish material ... Redistribute content from Credit Risk
     Analytics".
   - Both are in `license`. Whether a public collection may redistribute the file is your call.

6. **Probe gap.**
   - `generated_probes.py` does not flag the 5,000-row file. I ran it as a scratch definition: rule leaves cover 1.2%
     of the minority rows, no flag.
   - Drawing each feature independently within its class's range leaves neither mark the probe tests.
   - A within-class correlation check would catch it: mean |rho| 0.03-0.04 against a noise band of 0.09, and 0.21-0.42
     in the real rows. This fits the hepatitis_c_egypt agent's proposal, applied per class.
