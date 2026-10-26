# corporate_credit_rating_cat_data_set_ratings_raitings

**Outcome:** added. The book's own `ratings.csv` (197 rated institutions, most likely banks, each with six
financial ratios), not the generated OpenML 46372, as a regression on the rating code from 1 (AAA) to 10 with random
(IID) folds, scored with MAE (Lennart, 2026-10-21; RMSE before). The review panel recommends shipping after changes.

```text
Verdict: ship. Left: issues 2, 3 and 4 are open; the record's `problem_type` follows issue 2, and `source_links`
  is a record-field row.
Validity: SEL-16/PROV-3 hold as far as testable (within one code the ratios still move together, as real accounts
  do and the generated copy does not; no near-copies; the test for values drawn uniformly within a code cannot run, the largest code has 49 rows);
  PROV-13 applied (the book's file replaces the generated OpenML 46372); PROV-1/PROV-8 triggered in the record
  (`source_links` lead with the generated copy, field row); PROV-2 kept with a note (agency, period, country,
  rating type and possible modification not stated); USE-1 holds; USE-5 holds on the notch reading (supported by
  the data, unverified); USE-8 approximate (timing, scale, rating type, no country or support input); USE-3/LEAK-1
  cannot verify, no column shown to come after the rating; USE-10/USE-11/SPLIT-1 hold (one row per institution).
Value: TP-5/TP-8 not triggered for regression; TP-2 a small real signal (linear beats the mean on 100% of splits,
  ridge R² about 0.28 with a per-split SD of 0.097). Codes 1, 2 and 10 are 6.1% of the rows and 28% of ridge's
  squared error.
Quality: CLEAN-3 (`spid` dropped) holds; the size outlier kept with a note.
Weighed: size -, source + (the origin file), gap - (country, support, timing, scale), use case + (a shadow rating).
Licence: textbook use only, no commercial use, no redistribution; a note (EV-4), as for mortgage and lgd.
For the curator: issue 2 (the framing, a consistency check against corporate_credit_rating), issue 3 (chapter 8 of
  the book), issue 4 (the name).
```

**Main points:** Keep the regression on the code or ship 7 classes without codes 1, 2 and 10 (issue 2); obtain
chapter 8 of the book as a follow-up or before the public release (issue 3); keep or change the name (issue 4).

**Record fields that disagree with the definition:**

- `problem_type`: record `Multiclass Classification`, definition `Regression`.
- `source_links`: record `OpenML 46372, the Medium article, the Polanitz GitHub CSV, the book's data page`, definition `the book's data page and its ratings.csv link`.

**Record judgment:** valid with concerns. The rows are the book's own (Credit Risk Analytics, chapter 1, p. 14 and
Exhibit 1.4). OpenML 46372 and the Polanitz GitHub CSV are the same 5,000 rows generated from them (decided `No` on
the `_duplicate` record, 2026-10-12), yet they lead the record's `source_links`; the blind reviewer followed those
links and recommended exclusion, so the links mislead (the `source_links` row moves them to a comment line). The
`problem_type` row follows issue 2. The book names no agency, period, country or provider (issue 3).

**Issues for Lennart:**

2. **Regression on the 1-10 code (implemented), or 7 classes without codes 1, 2 and 10?** A consistency check. Your
   corporate_credit_rating framing, carried into corporate_issuer_credit_rating (CC 2026-10-16), uses letter
   classes with the rare grades merged or dropped, and your note on this record says "likely classification".
   - Implemented: regression on the 1-10 code, scored with MAE since 2026-10-21 (RMSE before; the curator's
     metric decision); the accepted warning records the reason.
   - Effect: regression scores how many notches a prediction is off; classes score only whether the exact code is
     hit, with no credit for one notch off. Option (b) also drops the top of the scale (AAA and AA+ under the notch
     reading) and the bottom code, so the 12 institutions at the ends are not rated.
   - Evidence: the codes hold {1: 3, 2: 5, 3: 14, 4: 32, 5: 37, 6: 49, 7: 23, 8: 18, 9: 12, 10: 4} rows, so as 10
     classes codes 1, 2 and 10 hold 1-2 rows per test fold (Too Small, TP-5). The source (a reader's
     transcription of the R Companion's chapter 8 code) fits an ordered logit, a classifier, and scores it by the
     absolute notch difference. Ridge R² is about 0.28 (RMSE 1.57 against 1.88 for the mean, 60 splits). Under
     regression the 12 institutions with codes 1, 2 and 10 (6.1% of the rows) carry 28% of ridge's squared error, so
     the score leans on them. Under option (b), 185 rows, the smallest classes hold 12 and 14 rows (4-5 per test
     fold), inside the band you kept under TP-8 on 2026-10-12 (four datasets, precedent
     check); codes 3 and 9 carry 22.5% of logistic regression's log loss for 14.1%
     of the rows, near their share.
   - What sets this case apart from corporate_credit_rating: there the letters were known, so a merge followed the
     rating convention (TP-7), and it had 2,029 rows; here only "1 = AAA, and so on" is known, and there are 197
     rows. wine_quality ships a 0-10 grade as regression because its paper models regression; here the analogy
     supports the distance metric, not the model class.
   - Rules: USE-5 (Must), TP-7 and TP-8 (Must). Neither framing breaks a Must on the evidence, so this is a
     weighing call. The advocate: the source scores in notches, the practitioner says 10 classes would throw away
     the order, and option (b) builds the target without a rating convention. The mediator: the only convention
     for (b) is the house practice of dropping classes under 10 rows (ecoli_proteins, lung_cancer), which is not a
     rating convention. The critic: your precedent and your note, the source's
     model is a classifier, and option (b) has no Too Small class.
   - Alternatives: (a) keep regression and record the facts above as the reason; cost: RMSE assumes equal notch
     steps, which is unverified. (b) 7 classes without codes 1, 2 and 10; cost: 12 rows and the ends of the scale.
     (c) Reopen corporate_issuer_credit_rating's framing to match; cost: a decided framing reopened. (d) Ship both,
     with a second `_clf` folder; cost: two tasks from 197 rows. A general rule for rating and grade targets is the
     cross-dataset item "When is a rating or grade target regression, and when classes?"; a rule adopted there
     settles this issue.
   - Recommendation (mediator): (a). The record's `problem_type` row follows this decision.
   - Decision: (a) regression, or one of (b) to (d).

3. **Obtain chapter 8 of the book (pp. 213-236): a follow-up, or a condition for the public release?** The data
   page and the book's chapter 1 (p. 14: "an anonymized data set with corporate ratings where the ratings have been
   numerically encoded (1 = AAA, and so on)") leave three things open: whether the financial statements precede
   the rating (the prediction point), which rating the label is (issuer or other) and whether a step is a notch or
   a letter grade, and whether the rows were modified (the same page says the book's LGD data were "slightly
   modified and anonymized"; the ratings entry names no provider). Chapter 8, whose R Companion code uses the
   data, is the only known source that could settle them, and it may say what the two ranges of `spid`, the anonymised institution id, are.
   - Effect: if the statements came after the rating, return on equity and costs to income could carry
     consequences of it (a leak of unknown, probably small strength); if the codes are letter grades, RMSE weighs
     unequal steps.
   - Evidence that nothing is wrong as far as it can be tested: no column is shown to come after the rating;
     holding out one of the file's two blocks gives ridge R² 0.262 against 0.255 for a random split of the same
     size; there are no near-copies (the nearest pair is 0.10 standard deviations apart); within one code the
     ratios still move together, as real accounts do and the generated copy does not; codes 7, 8 and 9 have median
     return on equity of 11%, 8% and 10%, which fits notches, not grades of CCC or worse. The test that flags
     values drawn uniformly within a class cannot run here (no code has 50 rows). The two `spid` ranges (130 and
     67 rows) differ a little in mean code and, within a code, on costs to income; holding one out costs no more
     than chance (split audit); no source explains them.
   - Rules: USE-3/LEAK-1 (Must) cannot be verified; PROV-2 (Should) keeps a plausible but unclear source with a
     note (bad_customer_detection); PROV-3 (Must) needs a finding, and a suspicion is a question (EV-3). By the
     rules this is a follow-up; it comes to you because EV-7 sends what cannot be verified to the curator.
   - Implemented: kept, with the fit `approximate` and notes on the timing, the rating type, the scale and the
     `spid` ranges.
   - Alternatives: (a) a follow-up: ship, and read chapter 8 when it can be obtained; cost: the three points stay
     unverified. (b) A condition: hold the public release until chapter 8 is read (the critic's position); cost:
     the release waits on a book we may not obtain, with no Must violation shown.
   - Recommendation (mediator, advocate): (a).
   - Decision: (a) a follow-up, or (b) a condition for the release.

4. **Keep the name, or rename before the first build?** The `unique_name` carries TabSTAR's label of the generated
   file: the typo "raitings" and "cat". "Corporate" is the book's own word (Exhibit 1.4 files the data under its
   "Corporate" risk segment, and p. 14 says "corporate ratings"), but the ratios (loan-loss provisions to loans,
   liquid assets to total assets) show banks; the book's Basel text lists banks and corporates as separate exposure
   classes, so "Corporate" reads as the book's non-retail segment.
   - Effect: none on the task; the name misdescribes the data to readers of the collection.
   - Rule: records.md, "names stay" (renaming breaks links and review marks), a house convention.
   - For keeping: the convention, and "Corporate" is the book's word. For renaming: the folder is not built, so a
     rename is cheap; churn_telco_nigeria was renamed while unbuilt (Lennart, 2026-10-15). A rename also changes
     the `_duplicate` record's name and the text of its CC. house_prices_nominal's issue 10 asks whether to keep a
     name for another reason (OpenML's name kept after a change of source) and recommends keeping it; the precedent
     check asks you to decide the two the same way.
   - Alternative: rename, for example to `credit_risk_analytics_bank_ratings`.
   - Recommendation: none from the mediator (the practitioner would name the entities as banks).
   - Decision: keep the name, or rename.

**Review panel:** ship after changes (mediator). Claim audit: 69 claims; refuted: one Spearman digit, "ridge beats
the random forest on 75% of splits" (61.7%), the record's "198" rows (197) and `problem_type`, and the probe-gap
issue of the earlier file; its row 54 ("refuted on attribution") is itself wrong, the quote is in the book's chapter
1; untested: the notch reading and the prediction point (both notes). Blind review: exclude; main
concern the provenance, after following the record's links to the generated copy, which the definition does not
use. Debate: agreed on the book's file, the random split, no leak, the note and number fixes and the licence as a
note; disputed: the framing (issue 2) and whether chapter 8 is a condition (issue 3). In the reports, the mediator's issues 1-3 and
"REVIEW issue" 2-4 are issues 2-4 here; their REVIEW issues 1 (OpenML), 5 (licence) and 6 (probe gap) are settled.

<details><summary>Mediator</summary>

**Mediator: corporate_cat**

**Recommendation (judgment record)**

```text
Verdict: ship after changes.
Validity: SEL-16/PROV-3 hold as far as can be tested (the ratios move together within a code, |rho| 0.21-0.29;
  no near-copies; uniform_within_class cannot run, largest code 49 rows); PROV-13 applied (the book's file replaces
  the generated OpenML 46372); PROV-1/PROV-8 fixed in the record (source_links); PROV-2 kept with a note (agency,
  period, country, rating type, possible modification not stated); USE-1 holds; USE-5 holds on the notch reading
  (supported by the data, unverified; the rating type is cannot-verify); USE-8 approximate (timing, scale, rating
  type, no country or support input); USE-3/LEAK-1 cannot verify, kept with the fit_reason note (no column shown to
  come after the rating); USE-10/USE-11/SPLIT-1 hold (IID, one row per institution).
Value: TP-5/TP-8 not triggered for regression; TP-2 a small real signal (linear beats the dummy on 100% of splits).
  The end codes 1, 2 and 10 are 6.1% of the rows and 28% of ridge's squared error (a note).
Quality: CLEAN-3 (spid dropped) holds; the size outlier is kept with a note; procedure numbers corrected.
Weighed: size -, source + (origin file), gap - (country, support, timing, scale), use + (shadow rating).
For the curator: issue 1, a weighing call on the framing (regression or option b), as a consistency check against
  corporate_credit_rating; issue 2, whether to look for chapter 8 (a follow-up); issue 3, the name.
```

**Changes to make now (no decision needed)**

1. **Record `source_links`** (PROV-1, PROV-8; precedents lung_cancer, miami_housing, nyc_taxi, and the sibling records lgd and mortgage):
   - Keep the book's data page `http://www.creditriskanalytics.net/datasets-private2.html` and the file URL.
   - Move OpenML 46372, the Polanitz GitHub CSV (the same generated 5,000 rows) and the Medium article to a comment line.
   - The blind reviewer followed the current links and recommended exclusion. That shows the links mislead readers.
2. **Other record fixes** (records.md; writing.md):
   - Change "Original has 198" to 197.
   - Set `problem_type` to the framing that ships. Leave it as it is until issue 1 is decided, then align it.
   - Keep the "From the book" quote. It is on p. 14 of chapter 1.
3. **Correct the false claim that the book was not read** (EV-7):
   - Correct "the book text was not read" in the accepted warning and in REVIEW issue 3.
   - Say chapter 1 was read and adds no agency, period, country or provider. On the same page, the LGD entry says "provided by a European bank ... slightly modified".
   - Change `fit_reason` "the data page gives only '1 = AAA'" to "the data page and the book's chapter 1 give only '1 = AAA, and so on'".
   - Correct claim audit row 54 ("refuted on attribution").
4. **Accepted warning** (precedents point 7):
   - Add one clause: the source fits an ordered logit and scores it in notches.
   - Say the wine_quality analogy supports the metric, not the model class.
5. **`fit_reason` / `task_summary.known`** (USE-5, USE-8):
   - Add "which rating (issuer or other) is not stated".
   - Add "no country or support input; size partly stands in for support".
6. **Real-data wording** (EV-3, EV-7):
   - In REVIEW issue 3 and anywhere else it appears, replace "pass the generated-data probe" / "pass the checks that caught HMEQ".
   - New wording: `uniform_within_class` cannot run (no code has 50 rows). The case rests on the ratios moving together within a code and on there being no near-copies.
   - Add the costs-to-income shift between the two `spid` ranges (p 0.004) to the `spid` bullet.
7. **Numbers** (writing.md, EV-7):
   - Liquid-assets Spearman: -0.39 becomes -0.38, in `_decisions`, curation_comments and REVIEW.
   - Ridge R²: 0.283 / 0.296 at alpha 1, or state the settings.
   - Block AUC: "0.52" becomes "about 0.43-0.48". Add that the codes differ a little between the blocks (Mann-Whitney p 0.049).
   - "Ridge beats RF on 75% of splits" becomes 61.7%.
   - Add the end-code error share to REVIEW. I re-measured it at 6.1% of the rows and 28% of ridge's squared error (3-fold x 20 repeats).
8. **"Corporate" against "bank"** (EV-2):
   - Write both in the note. The book files the data under its "Corporate" risk segment (Exhibit 1.4, a Retail/Corporate column) and says "corporate ratings" on p. 14. The ratios (loan-loss provisions to loans, liquid assets to assets) are bank ratios.
   - The book's own Basel text lists banks and corporates as separate exposure classes (chapter 1, the Basel section). So "Corporate" reads as the non-retail segment.
   - Exhibit 1.4 lists the Ratings data under chapter 5 (Credit scoring). The extracted chapter column is garbled, so whether chapter 8 also uses it cannot be read. The use_case's "as the book's chapter on low-default portfolios does" should say this comes from the R Companion code.
9. **REVIEW issues:**
   - Issue 1: state it as decided (Lennart, 2026-10-12, the `_duplicate` record).
   - Issue 6: drop it as stale. `uniform_within_class` flags OpenML 46372 (task_probes.md calibration, 2026-10-12).
   - Issue 5 (licence): make it a note (EV-4; mortgage and lgd carry the same terms with only a note). If redistribution matters for a public collection, it is one question for all the book's datasets.
   - Issue 2: rewrite it as the consistency check below. "Near the parkinsons line" and "the only framing with neither a Too Small class nor an assumed mapping" are both false.

**Issues for the curator (ranked)**

**1. The framing: regression on the 1-10 code (implemented) or option (b), 7 classes without codes 1, 2 and 10.**
- **Rank:** P3 (USE-5 Must) and P6 (TP-7, TP-8 Must). This is also a consistency check.
- **Problem and effect.** The implemented framing departs from your corporate_credit_rating / corporate_issuer_credit_rating framing (letter classes, rare grades merged or dropped; CC 2026-10-16). It also departs from your note on this record ("likely classification").
- **Why it is not settled by rank.** Neither framing breaks a Must on the evidence:
  - Regression keeps the source's labels and its distance scoring (`notchdiff`). TP-5 and TP-8 do not apply to it.
  - Option (b) passes TP-8. I measured it: codes 3 and 9 are 14.1% of the rows and carry 22.5% of logistic regression's log loss (22.4% for a random forest). That is near their share, unlike alvin's 51-54%. The smallest classes (12-14 rows, 4-5 per fold) sit inside the band you kept on 2026-10-12.
  - Option (b) builds the target. TP-7 asks for an established convention. The house practice of dropping classes under 10 rows (ecoli_proteins, lung_cancer) is the only one available, and it is not a rating-field convention.
  - Option (b) also cuts AAA/AA+ and the bottom code off the scale, which is a USE-5 cost.
  - "Which framing to ship" is a weighing call (principles.md, Weigh).
- **Advocate's best evidence:**
  - The source scores by notch distance.
  - The practitioner: "10 classes would throw away the order".
  - Only "1 = AAA" is known, so no merge can follow a rating convention.
  - 197 rows against 2,029.
  - wine_quality is the regression precedent.
- **Critic's best evidence:**
  - Your own precedent and your note on this record.
  - The source's model is an ordered logit, a classifier.
  - Option (b) has no Too Small class.
- **What would settle it:** the book's code-to-letter mapping (chapter 8), or a rule for ordinal targets.
- **Options:**
  - (a) Keep regression, with the facts that set this case apart recorded as the reason. This is my recommendation.
  - (b) Classification without codes 1, 2 and 10.
  - (c) Reopen the issuer rebuild's framing to match.
  - (d) Write a rule on when a rating or grade is regression.
  - (e) Ship both, as a `_clf` second folder.

**2. Chapter 8: a condition for release or a follow-up.**
- **Rank:** P4 (USE-3/LEAK-1 Must, cannot verify) and P5 (PROV-2 Should, PROV-3 Must).
- **Settled by rule as a follow-up:**
  - No Must violation is shown: no column comes after the rating, the block holdout gives 0.262 against a 0.255 control, and the rows pass the near-copy and formula tests.
  - PROV-2 keeps a plausible but unclear source with a note (bad_customer_detection).
  - A suspicion is a question (EV-3), and the remedy ladder stops at "keep with a note".
- **Why it still comes to you:**
  - EV-7 sends cannot-verify items to you: the prediction point, the rating type, and whether the rows were modified.
  - Chapter 1 settled none of them, so chapter 8 is the only known source.
- **Decision needed:** whether to obtain chapter 8 (pp. 213-236), and whether you want it before the public release anyway. Holding the release for it is your choice; the rules do not require it.

**3. The name.**
- **Rule:** records.md, "names stay" (house convention).
- **Effect.** The name carries TabSTAR's typo ("raitings") and "cat" from the generated file. "Corporate" matches the book's segment but not the entities, which are banks by their ratios.
- **For keeping it:**
  - records.md (renaming breaks links and review marks).
  - "Corporate" is the book's own word.
- **For renaming:**
  - Not built yet, so a rename is cheap now.
  - churn_telco_nigeria was renamed while unbuilt (Lennart, 2026-10-15).
  - A rename also touches the `_duplicate` record's name and CC text.
  - house_prices_nominal has the same open question; decide both the same way.
- **Decision needed:** keep the name, or rename (for example `credit_risk_analytics_bank_ratings`).

**Agreed facts**

- The file is the book's `ratings.csv`: 197 rows, sha256 `7cabb6bb...cfcc`, identical to the `.sas7bdat`.
- OpenML 46372 and the Polanitz CSV are a 5,000-row table generated from those 197 rows. Already decided as `No`/AHDS on 2026-10-12.
- Code counts are {1:3, 2:5, 3:14, 4:32, 5:37, 6:49, 7:23, 8:18, 9:12, 10:4}. 10 classes would be Too Small.
- The 1 = AAA direction holds in the data. The notch reading is supported (codes 7-9 have median ROE of 8-11%) but unverified.
- One row per institution. IID is right. No leak was found. The prediction point and the rating type cannot be verified.
- Signal is small but real: linear beats the dummy on 100% of splits. Ridge R² is about 0.28, with a per-split SD of 0.097.
- `uniform_within_class` cannot run here. The rows move together within a code and have no near-copies.
- The quote is in chapter 1, p. 14. Chapter 1 names no agency, period, country or provider.
- The licence is a note only (EV-4).

**Consistency with precedent**

- **Follows precedent:**
  - Issue 1 follows the `_duplicate` CC of 2026-10-12 and PROV-15.
  - The `source_links` repair follows lung_cancer, miami_housing and nyc_taxi.
  - Keeping a thinly documented source with notes follows bad_customer_detection and lgd.
  - Not applying the HMEQ and healthcare_insurance_expenses retirements is justified: the tests that failed there pass here.
  - The licence note follows mortgage and lgd.
- **Departs from precedent, as a question:**
  - The framing departs from corporate_credit_rating. Facts that set it apart: the letter mapping is unknown and there are 197 rows. That case was also retired under USE-5 on a measured finding (17% non-issuer labels); there is no such finding here.
  - The name departs from churn_telco_nigeria (renamed while unbuilt), so it is a question too.
- **For future cases:** this is the third time the low-cardinality warning has been accepted (wine_quality, numerai). The reason differs here, so no amendment is due. A short rule on ordinal targets would stop the two credit-rating tasks drifting apart.

Files: `datasets/_dev/tabarena-v0pt2/corporate_credit_rating_cat_data_set_ratings_raitings/dataset.py`, `curation/records/corporate_credit_rating_cat_data_set_ratings_raitings.md`, the publisher's chapter 1 excerpt (https://www.sas.com/storefront/aux/en/spcriskmdl/68835_excerpt.pdf): the Basel section, Exhibit 1.4 and p. 14. The TP-8 check script: (panel run).

</details>

<details><summary>Claim audit</summary>

**Claim audit: corporate_credit_rating_cat_data_set_ratings_raitings (2026-10-20)**

Data: raw `ratings.csv` (sha256 7cabb6bb...cfcc) and the definition frame via `dataset_io.from_definition` (197 x 7,
60 shipped splits, 20 x 3, IID). Evidence files from the 2026-10-07 run (sas7bdat, GitHub copies,
OpenML 46372 parquet, Polanitz 5k csv, R Companion Ch08 code, data page html, Crossref). Scripts and outputs: (panel run). Models untuned, sklearn defaults unless stated (EV-8).
Licence and pretraining overlap not used as evidence (EV-4).

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Task: rating from ratios | D task_summary | R Companion Ch08 code | holds | `polr(rating ~ COMMEQTA+...+SIZE)` under "MAPPING TO AN EXTERNAL RATING AGENCY" | USE-1 |
| 2 | Use case as the book's LDP chapter | D | same code; Crossref ch. title | holds (code, not book text) | Ch08 = "Low Default Portfolios", section 3 maps to an external agency; in-sample only in the code | USE-1, EV-2 |
| 3 | 197 institutions, 2016 | D row | count; Crossref | holds (count); "2016" is the book's year, not the data's | 197 rows, 197 unique spid; book issued 2016-10-03 | PROV-8 |
| 4 | Agency/years/country not stated | D | data page html | holds | page gives only "corporate ratings ... (1 = AAA, etc.)" and 6 definitions | PROV-8 |
| 5 | Code 1 (AAA)..10, notches | D | data page; ratio profile | 1 = AAA holds; notch reading untested | see 39 | USE-5 |
| 6 | Six ratios, definitions | D | data page vs RATIOS | holds | page lists exactly these 6 with these meanings | CLEAN |
| 7 | Split: random institutions, same period | D | splits; dup check | holds as stated (period untestable) | 60 IID splits, test 65-66; no institution twice | SPLIT-1 |
| 8 | 197 rows, not 5k OpenML | D | definition frame | holds | frame 197 x 7 | PROV-13 |
| 9 | Code predicted as number | D | problem_type | holds | regression | TP-7 |
| 10-11 | fit approximate; notch not verified | D | data page | holds | no dates, only "1 = AAA" | USE-8 |
| 12 | year 2016, finance, Other, URL | D | Crossref | holds (publication year) | | PROV-8 |
| 13 | Licence text | D | not evidence | not audited | | EV-4 |
| 14 | File link needs no login, HTTP 200 | D | `curl -I` today | untested (rate-limited) | HTTP 429 at 16:35 today; preparation saw 200 | |
| 15 | sas7bdat same 197 rows | D | read_sas, align by spid | holds | max abs diff 0.0 | PROV-2 |
| 16 | GitHub copies same sha256 | D | sha256 | holds | dpicone1 and jlzml copies 7cabb6bb...; redownload same | PROV-2 |
| 17 | sha256 | D | sha256 | holds | 7cabb6bb...cfcc | |
| 18, 23, 24, 58 | OpenML 46372 generated uniformly within per-code min-max; none a book row | D, R | range test, midpoints, row match, within-code rho | holds | 30,000/30,000 values inside ranges; class means within 3% of range midpoint; 0 book rows; 500 per code; within-code mean abs Spearman 0.026-0.042 vs 0.21-0.29 (codes 3-9 real); OpenML features = Polanitz 5k csv | PROV-3, SEL-16 |
| 19 | bibtex | D | Crossref | holds | DOI 10.1002/9781119449560, ISBN 9781119143987, Wiley 2016, Baesens/Rösch/Scheule | |
| 20 | Intro facts | D | counts | holds | 197, unique spid, quote matches page | |
| 21 | Ordered logit in Ch08 code | D | code | holds | `polr` (MASS) | |
| 22 | Statement vs rating date unknown | D | page | holds | no dates anywhere | LEAK-1 |
| 25 | Target rating_notch, RMSE | D | definition | holds | | |
| 26 | Code scores by notch difference | D | code line 63 | holds | `notchdiff <- abs(as.double(rating) - as.double(prediction))` | TP-7 |
| 27, 47, 50 | Codes 1, 2, 10 hold 3, 5, 4 | D | value_counts | holds | {1:3, 2:5, 10:4} | TP-5 |
| 28 | spid undocumented | D | page | holds | not on the data page | CLEAN |
| 29 | spid two ranges | D | min/max | holds | 100,079-130,277 (130); 300,021-453,328 (67) | |
| 30 | Range flag lifts ridge R² 0.286 -> 0.299 | D | ridge on 60 shipped splits, alpha 0.1/1/10, OLS | holds in direction; digits not reproduced | 0.281->0.295 (a0.1), 0.283->0.296 (a1), 0.289->0.303 (a10), OLS 0.281->0.294 | EV-8 |
| 31 | Renamed after page | D | | holds | | |
| 32 | No NA, no duplicates | D | | holds | 0 NA, 0 dup with/without spid | LEAK-16 |
| 33 | Negative LLP/ROE real | D | counts; plausibility | holds (counts); "real" untestable | 7 LLP (min -0.002), 30 ROE (min -0.50) | CLEAN |
| 34 | Two sorted blocks 98/99, no institution in both | D | diff of rating order | holds | one decrease at row 98; spid unique | |
| 35 | RF cannot tell blocks apart (AUC 0.52) | D | RF 500 trees, 5-fold | holds; digit not reproduced | AUC 0.43 (ratios), 0.44 (with rating). But codes differ a little: Mann-Whitney p 0.049, permutation on means p 0.11, chi2 p 0.13; block x spid range p 0.063; LIQASSTA KS p 0.039 (1 of 6) | EV-9 |
| 36 | Base class shuffles | D | preprocessing.py; frame order | holds | `order_rows` seed 42; frame starts 8,5,5,5,6,... | |
| 37 | SIZE 10.59 vs 15.33 | D | sort | holds | code 8 | |
| 38 | Ridge fits it; unit slip fits worse | D | ridge a1, outlier's test-fold error over the 20 folds that hold it; shift SIZE by ln(100)/ln(1000) | holds | mean error -0.27 (abs 0.60) as is; -2.99 / -4.35 shifted; mean R² 0.283 -> 0.266 / 0.248 | CLEAN |
| 39, 42, 11 | Codes are notches (AAA..BBB-) | D | the book text is the decisive test; not available | untested | supporting only: code 10 median ROE 2.8%, LLP 1.1% (not defaulted banks) | USE-5, EV-7 |
| 40 | 57 rows codes 7-10 | D | count | holds | 57 | |
| 41 | Median ROE codes 7/8/9 = 11/8/10% | D | medians | holds | 11.4/8.3/10.2% | |
| 43 | Entities are banks | D | ratio levels | holds (circumstantial) | median equity/assets 5.9% (max 31.8%), LLP/loans and liquid assets/assets are bank ratios | PROV-8 |
| 44 | NN agreement 25.5% vs 22.4% | D | 1-NN over 60 splits, standardised on train | holds | 24.8% vs 22.8%; min NN distance 0.10 std units, median 0.71: no near-copies | LEAK-21 |
| 45-46 | Accepted warning reasons; wine_quality precedent | D | wine_quality definition | holds | wine_quality `problem_type = "regression"` | TP-7 |
| 48 | Spearman -0.50/-0.39/+0.26/+0.20/-0.17/+0.10 | D `_decisions` | spearmanr | refuted on one digit | liquid assets -0.3846 (rounds to -0.38); others match | writing |
| 49 | Ratios move with code as 1 = AAA should | D `_decisions` | sign of each Spearman under 1 = AAA vs reversed | holds for orientation, one exception | size, liquidity, LLP, ROE, cost/income agree with 1 = AAA; equity +0.26 runs the other way (definition explains it by size); reversed coding would need bigger banks rated worse | USE-5 |
| 51 | No splits_comment, IID | D | README | holds | | |
| 52 | Record problem_type Multiclass | R | vs D | refuted (conflict) | D is regression | PROV-1 |
| 53 | Derived from the book via Medium | R | data match | holds for the book file; the Medium/OpenML file is a generated derivative | | PROV-3 |
| 54 | "From the book:" quote | R | data page html | refuted on attribution (wrong, corrected by the mediator: the sentence is also in the book, chapter 1, p. 14) | the sentence is on the data page `datasets-private2.html`; book text not read | PROV-8 |
| 55 | Original has 198 | R | row count | refuted | 197 rows (198 lines with header) | PROV-8 |
| 56 | Modified by the Medium author | R | Polanitz notebook | untested | notebook loads 5,000 rows, no generation code; who generated it is unknown | EV-7 |
| 57 | Likely classification | R | logistic 10-class vs prior | weighing, facts below | see 65 | TP-5 |
| 59 | OpenML 1 = "very_bad" | R | align OpenML rows to Polanitz numeric file | holds | very_bad=1 ... outstanding=10 (reverse of 1 = AAA) | PROV-3 |
| 60 | R assessment facts | R | as 26, 27, 43 | holds | | |
| 61 | Terms | R | not evidence | not audited | | EV-4 |
| 62 | Priority 1 reasons | R | weighing | not a factual claim | | |
| 63a | Ridge R² 0.286, RMSE 1.57 vs 1.88 | REVIEW | 60 splits | holds approx. | 0.283 (a1) / 0.289 (a10); RMSE 1.567 vs 1.882 | EV-8 |
| 63b | Ridge beats RF on 75% of splits (SE 0.012) | REVIEW | RF 300 trees default vs ridge a1, per-split RMSE | refuted on the number | 61.7% (37/60), paired SE of R² diff 0.015; direction holds (mean R² 0.283 vs 0.227) | EV-8 |
| 64 | Codes 1/2/10: 1-7 per fold, median 4, 6% rows, 29% of SE | REVIEW | ridge a1 | holds | 1/4/7, 6.1%, 28.8% | TP-5 |
| 65 | Logistic 10/7/3-class log loss and AUC | REVIEW | logistic, 3-fold x 10 | holds | 1.891 vs 2.023 AUC 0.678; 1.684 vs 1.837 AUC 0.721; 0.834 vs 0.986 AUC 0.766; groups 54/109/34 | EV-5 |
| 66 | Mean code by range 6.24 vs 5.36, p 0.001 | REVIEW | Mann-Whitney | holds | p 0.0014 | |
| 67 | NN distance does not predict code (R² -0.12) | REVIEW | OLS code ~ NN distance, 3-fold x 20 | holds (digit differs) | R² -0.05 | |
| 68 | Ch. 8 pp. 213-236 | REVIEW | Crossref | holds | "213-236" | |
| 69 | generated_probes.py does not flag the 5k OpenML file | REVIEW issue 6 | crosscut output 2026-10-12; current `curation_probes/generated.py` | refuted (stale) | the probe now has `uniform_within_class` (generated.py:414); on 46372 it flags all three frames: 60 of 60 within-class cells uniform, 4.0% of pairs dependent; the 197 rows have no flag | PROV-3, SEL-16 |

**Unwritten claims**

| Claim | Test | Result | Rule |
|---|---|---|---|
| Every feature is known at the prediction point | needs statement and rating dates | untested (cannot verify; already the fit_reason) | LEAK-1, USE-3 (Must) |
| The split is the one the use case needs | IID vs alternatives: no time, no group column; blocks not separable by features (AUC 0.43) | holds as far as testable | SPLIT-1 |
| The target is the real-world target | agency rating code, 1 = AAA | holds in orientation; scale step (notch) untested | USE-5 |
| No row is a copy across the split | exact and 1-NN | holds | 0 duplicates; nearest pair 0.10 std units; NN agreement 24.8% vs 22.8% | LEAK-16 to LEAK-21 |
| The book's file is unmodified real data | generated probe; within-code dependence | holds as far as testable (no flag; within-code rho 0.21-0.29); book says the site offers "real and simulated" data (search result, not this file) | SEL-16, PROV-3 |

**Refuted and untested, ranked (principles.md)**

1. Untested, P4 Must (LEAK-1): statement date vs rating date. Changes nothing now (fit=approximate says it). Remedy: keep the note; settle from chapter 8.
2. Untested, P3 (USE-5): notch reading of the 10 codes. Remedy: keep the note; chapter 8.
3. Refuted, P5 record (PROV-1): record `problem_type: Multiclass Classification` vs regression; record says "198" (is 197); quote attributed to "the book" is from the data page. Remedy: correct the record lines at the curator's verdict.
4. Refuted, procedure: REVIEW issue 6 "Probe gap" is stale; the current probe flags OpenML 46372 (`uniform_within_class`). Remedy: drop or rewrite issue 6.
5. Refuted, procedure (EV-8): "ridge beats RF on 75%" is 61.7% here; ridge 0.286/0.299 and block AUC 0.52 depend on unstated settings; Spearman -0.39 is -0.385. Remedy: state the model settings with each number or round (e.g. "about 0.28 to 0.30"); -0.38.
6. Untested: file URL HTTP 200 (429 today); "modified by the Medium author" (no generation code in the notebook).

</details>

<details><summary>Column audit</summary>

**Column audit: corporate_credit_rating_cat_data_set_ratings_raitings (2026-10-20)**

Frame loaded through `dataset_io.load(..., built=False)` (origin `definition`): 197 rows, 7 columns, no missing values.
Codebook: the book's data page (fetched today): "an anonymized data set with corporate ratings", "numerically encoded
(1 = AAA, etc.)", and one-line definitions of the six ratios; `spid` and `rating` are not defined. Prediction point
(first `curation_comments` bullet): statements known, agency rating not; statement date vs rating date unknown.
Scripts: (panel run).

**Column table**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `rating_notch` (target; raw `rating`) | rating code, "1 = AAA, etc."; the step size (notch vs letter grade) is not stated | target | int64, 1-10, counts 3/5/14/32/37/49/23/18/12/4; regression. Not skewed, no cap, no missing | question for the curator: equal-notch distance is unverified, so RMSE weighs an unknown scale (already REVIEW issue 2) | USE-5, TP-7, CLEAN-17 |
| `spid` (dropped) | undefined; an anonymised institution id | n/a | 197 unique; two ranges (100,079-130,277: 130 rows; 300,021-453,328: 67 rows). Within a range the id does not order the code (Spearman +0.16 / -0.23, p 0.07 / 0.06) | fine to drop. Not a label-encoding id; the range flag is a possible population marker (+0.013 R²), undocumented | CLEAN-3, LEAK-10 (not triggered), LEAK-33 |
| `common_equity_to_total_assets` (COMMEQTA) | common equity / total assets | yes if the statements precede the rating (unknown) | float64, 0.007-0.318, 6 decimals; no proxy codes. Max 0.318 is the tiny-size row (see below) | fine | CLEAN-14 |
| `loan_loss_provision_to_total_loans` (LLPLOANS) | loan-loss provision / total loans | as above | float64, -0.0017-0.095; 7 negative (provision releases), 2 exact 0 (codes 2 and 4; plausible, not a sentinel) | fine | CLEAN-10, CLEAN-11 |
| `operating_costs_to_operating_income` (COSTTOINCOME) | operating costs / operating income | as above; a same-period cost ratio could partly reflect a rating change (funding costs) if the statements post-date the rating | float64, 0.047-2.47; 5 rows > 1, three of them with positive ROE (0.06-0.11): unusual, not impossible (non-operating income) | fine; keep (unusual, not impossible). Differs between the `spid` ranges within a code (-0.095, p 0.004) | CLEAN-11; LEAK-1 question |
| `return_on_equity` (ROE) | return on equity | as above; same timing caveat as costs/income | float64, -0.50-0.50; 30 negative (loss years). Implied ROA (ROE x equity ratio) -1.6% to 5.6%, plausible for banks | fine | CLEAN-11; LEAK-1 question |
| `liquid_assets_to_total_assets` (LIQASSTA) | liquid assets / total assets | as above | float64, 0.007-0.82 | fine | CLEAN-14 |
| `log_total_assets` (SIZE) | natural log of total assets (unit and currency not stated) | as above | float64, 4 decimals (other ratios 6); exp gives 40k-2.0bn, so the unit is likely thousands (median 66bn). Row spid 117051 (code 8): 10.59 vs next 15.33, with the file's highest equity ratio 0.318: consistent with a genuinely small institution; a x1000 slip would give 17.5 | fine; outlier kept with its note. No within-code shift by `spid` range big enough to suggest a second unit (-0.33 log, p 0.13) | CLEAN-11, CLEAN-21 |

No column is constant, a copy, an object dtype or scaled over all rows (ratios in natural units; SIZE a per-row log):
CLEAN-5, CLEAN-9, LEAK-30 / probe 16 not triggered. Shipped row order is shuffled (next-row same code 14% vs 91% in
the raw file; position vs code Spearman 0.02): CLEAN-23 holds. Rounding is the same in both file blocks and both id
ranges (probe 9 analogue): no format artefact.

**Problems, ranked (principles.md)**

1. **P4, LEAK-1 / USE-3 (question, not a leak).** No column is known to post-date the rating, but no source gives the
   statement date relative to the rating date. If the ratios are from the same or the following fiscal year, ROE and
   costs/income could carry consequences of the rating (funding cost); strength unknown and probably weak. No probe can
   settle it; chapter 8 of the book could. Mildest remedy: keep `fit="approximate"` with the stated gap (already
   there); no column change.
2. **P3, USE-5 / TP-7 (target scale).** `rating_notch` as a number assumes equal notch steps; only "1 = AAA" is
   documented. The data favour notches (codes 7-9 median ROE 8-11%). Remedy: keep with the existing note; settle from
   the book.
3. **P4/P5, CLEAN-3 (`spid` ranges).** Dropping is right for an undocumented id, and it does not encode the label
   within a range. The ranges differ within a code on costs/income (p 0.004) and slightly on size, so they may be two
   populations or two data vendors with different cost definitions. Remedy: keep dropped; mention the costs/income
   shift in the existing `spid` bullet so the curator sees what the flag captures.
4. **P7, CLEAN-11 (`log_total_assets` outlier).** Kept correctly; supporting fact for the note: the same row has the
   highest equity ratio, as a very small institution would.
5. **P7, notes accuracy.** "next smallest 15.33" holds (15.3274). No cleaning problem found in any column.

Verdict: no leak, no cleaning problem; two questions for the curator (prediction point, target scale) already in
REVIEW.md.

</details>

<details><summary>Split audit</summary>

**Split audit: corporate_credit_rating_cat_data_set_ratings_raitings (2026-10-20, re-check)**

**Verdict: right with notes.** IID, 20 repeats x 3 folds (seed 4267), train 131-132, test 65-66 rows.

Scripts and data: (panel run). Ridge = StandardScaler + Ridge(alpha 1); RF = 300 trees, min leaf 3.

**Regime against the use case**

- Use case: a shadow rating for an institution that has no agency rating (task_summary). That is a new entity, a cold
  start (USE-10), and the file has one row per institution (197 unique `spid`, 0 duplicate rows), so USE-11 makes it IID
  without grouping. Declared regime: IID. Matches. SPLIT-1, SPLIT-2 hold.
- No time column, no statement or rating dates, no period stated. Not a stream of readings (SPLIT-7 does not apply):
  a cross-section of ratings. SPLIT-8 (forced IID from temporal) is not triggered, since nothing in the release is a
  status standing in for a forecast; the missing period is a use-case gap already carried by `fit="approximate"`.

**Hidden groups and near copies (SPLIT-29, SPLIT-30, LEAK-16 to LEAK-21)**

- Hidden-group probe: no candidate column, 0 composite keys, 0% of rows in near-copy clusters at 0.7-0.9. No hit.
- Repeated institutions under new ids (e.g. the two file blocks as two years of the same banks)? Tested: cross-block
  pairs with |SIZE diff| < 0.05 and |equity-ratio diff| < 0.01: 40 (of 9,702 pairs), within-block 31 (of 9,604), and
  only 7.5% of the cross-block pairs share the code (29% within block, 22.4% for all nearest neighbours). Ratings are
  sticky year to year, so the same bank a year later would mostly keep its code; these pairs do not. Mutual nearest
  neighbours: 45 pairs, code agreement 22%, mean |code diff| 1.33. No repeated entity across the split.

**Alternative splits run (mean over directions; R² ridge / RF; dummy RMSE)**

| Split | ridge R² | RF R² | dummy RMSE |
|---|---|---|---|
| Shipped 60 IID splits | 0.283 (SD 0.097) | 0.234 (SD 0.104) | 1.88 |
| File block held out (98 / 99, both directions) | 0.262 | 0.281 | 1.90 |
| Random 50/50 control (40 splits) | 0.255 | 0.248 | 1.89 |
| `spid` range held out (130 / 67, both directions) | 0.191 | 0.219 | 2.04 |
| Random 130/67 control (40 splits) | 0.215 | 0.227 | 1.89 |

- Block holdout costs nothing against a size-matched random split (0.262 vs 0.255); a RF cannot tell the blocks apart
  from the ratios (ROC AUC 0.48). If the blocks were two periods, there is no measurable shift.
- `spid` range holdout: -0.024 ridge, -0.008 RF against the size-matched control, within the per-split SD (~0.1).
  RF tells the ranges apart from the ratios only weakly (ROC AUC 0.584).

**Problems, ranked (principles.md)**

1. **P4, note: unknown period, so the test cannot stand for later institutions (SPLIT-7/SPLIT-8 boundary, USE-9).**
   Evidence: no dates anywhere; the block holdout, the only possible period proxy, shows no drop (0.262 vs 0.255).
   Remedy: none in the split; keep the existing wording ("other institutions of the same unknown period") and
   `fit="approximate"`. If chapter 8 of the book gives years, re-check for a temporal split.
2. **P4, note: two `spid` ranges as possible sub-populations (SPLIT-29, SPLIT-30, SPLIT-31).** Evidence: 130 / 67 rows,
   mean code 5.36 vs 6.24; holding a range out costs 0.008-0.024 R², within noise. It is a population, not an entity
   repeated across rows, and the source does not call it a group. Remedy: none; keep IID. A range-held-out variant
   would be a domain-shift test with two groups (the "only a few groups" factor, covertype), not a fix.
3. **P6/P4, note: small, noisy folds.** Test 65-66 rows, per-split ridge R² SD 0.097; codes 1, 2, 10 hold 12 rows in
   total. 20 repeats is the right answer; no change. Unstratified folds are fine for regression.
4. **Procedure, minor:** ridge R² at alpha 1 on the shipped splits is 0.283, not the 0.286 in `curation_comments`
   (matches the checklist's re-measure); state the ridge settings or round.

Judgment: SPLIT-1, SPLIT-2, USE-10, USE-11 hold; SPLIT-29/30 not triggered (no hit, alternative within noise);
LEAK-16 to LEAK-21 hold (no copies, no repeated institutions). Mildest remedy for every item: none or a note.

</details>

<details><summary>Domain practitioner</summary>

**Practitioner: corporate_credit_rating_cat_data_set_ratings_raitings (2026-10-20)**

Actor: a credit analyst in a bank's counterparty (financial institutions) risk unit. I need a rating for a bank we
lend to or trade with that has no agency rating, or an internal rating anchored to the agency scale (a shadow rating
for a low-default portfolio under IRB). I build the shadow rating model on banks that do have an agency rating and
apply it to unrated ones. Moment: when the counterparty is onboarded or reviewed, with its latest annual statements.

**Fit: approximate (agree with the definition)**

Mapping bank ratios onto an agency scale is a real, current practice (shadow rating for low-default bank exposures),
but the data omit the country and support inputs that drive bank ratings, and the timing between the statements and
the rating is unknown (USE-8: a label without a stated date relation). USE-9 gives no direct reframing: the shadow
rating of an unrated bank *is* the use case, and rephrasing it would only excuse the gaps (weighed factor against
USE-9).

**1. Inputs at the prediction point (USE-3, USE-6)**

Inputs I would have (all six are legitimate, USE-6): equity/assets, loan-loss provisions/loans, cost/income, ROE,
liquid assets/assets, log total assets. All come from published statements, so no leak as long as the statements
precede the rating date (unknown, see gap 3).

Inputs I would always have and that are missing, ranked:
1. Country / the sovereign rating and the banking-system risk (S&P's anchor from BICRA; Moody's macro profile). A bank
   is rated from its country's anchor upward or downward, and is usually capped near its sovereign. Without it the
   same ratios mean different ratings in Germany and in Italy. This is the largest gap.
2. Support: government or group (parent) support. Agency issuer ratings of banks add up to about 3 notches for
   systemic importance (S&P's ICR = SACP + support). In this data `log_total_assets` is the strongest predictor
   (Spearman -0.50), which I read as partly a too-big-to-fail proxy for support, not stand-alone strength.
3. Asset quality stock measures (NPL or impaired loans ratio), regulatory capital (CET1 / Tier 1 ratio, not just
   book equity/assets), funding mix (loans/deposits, wholesale funding). The loan-loss provision ratio is a flow,
   noisy year to year (the data hold negative values from releases).
4. The previous rating, for banks already rated (USE-10). Not relevant for the unrated-bank use case, so its absence
   is correct here.

Inputs I would not have: none of the six is post-outcome.

**2. Target (USE-5)**

I act on the issuer rating (pattern under USE-5) mapped to a PD on my master scale. The code 1 (AAA) to 10 is what I
want if it is the issuer rating in notches; whether it is the issuer rating, the stand-alone profile, or a debt
rating is not stated. The 10 codes fit an investment-grade notch scale AAA..BBB- (typical of rated banks before
2008/2016) far better than letter grades: codes 7-9 have median ROE 8-11%, which no CCC bank has. So the notch
reading is the plausible one, still unverified.

What I want predicted: a notch (or the distribution over notches, to read the PD band). A number on the notch scale,
scored by error in notches, is how I validate a shadow model (hit rate within +/- 1-2 notches). RMSE on the code is a
reasonable proxy; the mean absolute notch error is what I would report. Regression is the right framing; 10 classes
would throw away the order (and three codes hold 3-5 rows).

**3. Row and split (USE-10, USE-11)**

One row = one rated bank at one (unstated) date, the right unit for a shadow rating: one decision per counterparty.
USE-11: the use case is the first rating of a new counterparty, so one row per entity and IID is acceptable (the 197
ids are unique). USE-10: a cold start is what I face (an unrated bank), so a random split by institution mirrors it.
What I would really face differs: the development sample is the rated banks of one or more years, and I apply the
model to unrated banks next year, which are smaller and often from other countries. The random split tests neither
the shift in time nor the shift from rated to unrated (smaller) banks; it stays approximate (USE-8).

**4. Would I use it?**

As a benchmark task: yes, it is a recognisable textbook version of a real model. As my production model: no.
- Trust: the ratios move with the code the way bank analysis expects (bigger and more liquid banks rated better;
  higher provisions, higher cost/income rated worse); R^2 ~0.29, an error of about 1.6 notches RMSE is the order of
  accuracy a ratio-only shadow model reaches without country and support.
- Distrust: no agency, years or country; I cannot tell if the statements precede the rating; the `spid` id ranges
  may mark two populations (two agencies, regions or years) that my model would mix; 197 banks is a realistic size for
  a bank shadow-rating sample, but the tails (codes 1, 2, 10) have 3-5 banks, so the extremes are guesses.
- The equity/assets sign (+0.26 with a worse code) is the opposite of a stand-alone view and fits a support story:
  large, thinly capitalised banks get higher ratings because of support. That is real agency behaviour, but it
  shows the label is the supported issuer rating, which a model without support inputs imitates through size.

**Gaps ranked by how much they change the task**

1. No country / sovereign anchor (changes the task most; the model cannot learn the anchor and the cap).
2. No support input; size stands in for it.
3. Timing between the statements and the rating unknown (USE-3; potential leak only if statements postdate the
   rating, harmless for a cross-section read as concurrent).
4. Scale unverified (notch vs letter; issuer vs other rating) (USE-5).
5. Random split vs the real shift (next year, unrated and smaller banks).
6. Possible two populations hidden in the id ranges.

**What an expert would change**

- Add the country or the sovereign rating and a support flag (government-related, systemically important, subsidiary
  of a rated group) if any source gives them; without them, say in `task_summary.known` that country and support are
  absent and that size partly stands in for support.
- Report the error in notches (MAE, share within +/-1 notch) alongside RMSE where the collection allows.
- Name the entities as banks in the `unique_name` (the record says "corporate"), as REVIEW.md issue 4 proposes.
- If chapter 8 of the book is obtained: confirm issuer rating, agency, period, and whether the two id blocks are
  development and validation samples; if they are, a split along the blocks is the realistic test.
- Keep `spid` dropped; keep regression; keep approximate.

**Sources**

- Definition and record: `datasets/_dev/tabarena-v0pt2/corporate_credit_rating_cat_data_set_ratings_raitings/dataset.py`,
  `REVIEW.md`, `curation/records/corporate_credit_rating_cat_data_set_ratings_raitings.md`; panel `claims.md`,
  the clean-room data (panel run; per-code medians re-read).
- `.claude/skills/knowledge-curation/references/use_case.md` (USE-3, USE-5, USE-6, USE-8, USE-9, USE-10, USE-11).
- S&P bank rating framework (anchor from BICRA, SACP, government support up to 3 notches):
  https://www.bondadviser.com.au/blog/breaking-down-the-sp-bank-credit-rating-framework/ ;
  https://spglobal.com/ratings/en/research/articles/250428-banking-industry-country-risk-assessment-update-april-2025-13482604
- Shadow rating for low-default portfolios: https://media.abieventi.it/eventi/3E42EF6B-5FF0-4A8C-A9BE-0FD9226D3229/relatori/20260611163955RIZZO_S&P_%20ABI%20June%202026.pdf ;
  https://www.crisil.com/en/home/our-businesses/global-research-and-risk-solutions/our-offerings/credit-and-lending-solutions/credit-risk-consultancy/case-studies/partnered-with-a-g-sib-for-rating-scorecard-development.html ;
  https://oliverwyman.com/our-expertise/insights/2024/nov/how-to-improve-irb-modelling-for-low-default-portfolios.html
- Book: https://www.kdnuggets.com/2018/03/baesens-book-credit-risk-analytics-r.html (R Companion, LDP chapter).

</details>

<details><summary>Blind review</summary>

**Blind review: corporate credit rating (bank ratios -> rating notch)**

**Verdict: exclude.** The prepared table cannot be traced to the public sources it cites, and it is too small to score reliably.

**Task**
The task is to predict a bank's credit rating notch (1-10) from six balance-sheet ratios. A credit analyst or a bank's internal rating model could use this to shadow-rate unrated banks, so the use is real. The split is IID with no time or issuer grouping. That is defensible only if every row is a different bank in the same year, and I could not check that.

**Concerns (most serious first)**
1. **Provenance does not match.**
   - The cited GitHub `ratings.csv` and OpenML 46372 both have 5000 rows, with exactly 500 per class (10 classes).
   - The prepared data has 197 rows with an unbalanced target: 3/5/14/32/37/49/23/18/12/4.
   - Matching rows on COMMEQTA (rounded to 5 decimals) finds only 52 matches. On those, the target agrees 11% of the time, which is chance level.
   - The column means also differ. For example, LLPLOANS has a mean of 0.0077 here against 0.0199 in the source.
   - So the table comes from some other, undocumented extract. The perfectly balanced 5000-row public version is itself suspicious: it looks resampled or generated (31 spid duplicates).
   - Change: document the true source and how rows were selected, or rebuild from a verifiable original.
2. **Too small.** At 197 rows, each test fold holds about 66 rows. Cross-validated R2 is 0.27 for ridge and 0.21 for random forest, so method rankings will be mostly noise.
3. **The target's direction is unclear.** OpenML labels 10 as "outstanding", but in the source a higher number goes with higher cost-to-income (r=+0.47) and higher loan-loss provisions (r=+0.37). That means higher numbers are worse ratings, and the label names look reversed.
   - Change: state the scale explicitly.
4. **Minor.** There are no exact duplicates and no missing values. All values are plausible ratios and log assets.

**Not checked**
- The book's original data (it sits behind the creditriskanalytics.net private download).
- The rating agency, the year, and whether any bank appears more than once.

</details>

<details><summary>Precedent check</summary>

**corporate_credit_rating_cat: precedents**

Precedent check for the review panel (re-check), 2026-10-20. Inputs read:
- the panel's inputs (the earlier REVIEW.md, the checklist, the claims list, the probes; panel run);
- the run's register of decisions (panel run);
- the definition `datasets/_dev/tabarena-v0pt2/corporate_credit_rating_cat_data_set_ratings_raitings/dataset.py`;
- the records under `curation/records/`: this one, `_duplicate`, `corporate_credit_rating`, `corporate_issuer_credit_rating`, `lgd`, `mortgage`, `homeq_default_prediction`, `healthcare_insurance_expenses`, `wine_quality`;
- the knowledge files: `principles.md`, `selection.md`, `provenance.md`, `task_probes.md`, `records.md`, `definitions.md`;
- the git history of the records, and `CHANGELOG.md`.

I could not read Lennart's marks on the review-page artifacts (no ArtifactData tool). If he marked this dataset there, those marks come first.

**Verdict per decision or issue**

| # | Decision / issue | Status | Closest precedents |
|---|---|---|---|
| 1 | OpenML 46372 is generated; use the book's file | consistent; already decided | `_duplicate` record, CC 2026-10-12 Lennart: "No: generated data (AHDS), a simulated copy of the book's rows". PROV-15 Cases row "OpenML 46372: a problem of that copy". PROV-15 "TabSTAR's version … no reference for ours" (2026-10-15, Lennart) |
| 1b | Record `source_links` fix | consistent, needs no decision; the issue understates it | lung_cancer, miami_housing, immoscout: OpenML copy links removed when the definition uses the original (commit 2475ea2, 2026-10-14). nyc_taxi_trip_duration, melbourne_housing_market: related links moved out of `source_links` (58ee235, 2026-10-20, curator's review). Siblings lgd and mortgage list only `http://www.creditriskanalytics.net/datasets-private2.html` |
| 2 | Regression on the code instead of classes | departs from the curator's leaning and from his credit-rating precedent, with a stated reason; the precedent is not named and option (b) is misread against TP-8 | wine_quality (regression on a 0-10 grade with grade 9 at 5 rows; Lennart CC 2026-09-30). corporate_credit_rating (6 letter classes, CCC/CC/C merged, AAA and D dropped; carried into corporate_issuer_credit_rating by Lennart CC 2026-10-16). ecoli_proteins and lung_cancer (classes under 10 rows dropped). TP-8 keeps of 2026-10-12. parkinsons (TP-5, 2026-10-05) |
| 2b | Record `problem_type` differs from the definition | consistent handling | records.md and definitions.md: the record follows the framing that ships. Alignments in 2475ea2 (aeolus, asp_potassco_classification, qsar_aquatic_toxicity) and 58ee235 (coad). lgd REVIEW issue 1: the same mismatch, put to the curator |
| 3 | Provenance gaps; kept with notes | consistent; one claim is not accurate ("book text was not read") | bad_customer_detection (PROV-2, kept with a note, Lennart 2026-10-14). homeq_default_prediction (retired 2026-09-24: near-copy clusters; not present here). healthcare_insurance_expenses (retired 2026-10-06: a formula; not present here). lgd REVIEW issue 5 ("slightly modified" left open) |
| 4 | Name kept | consistent with the default; the alternative has a precedent | records.md: "names stay". churn_telco_nigeria renamed to `churn_telco_south_asia_duplicate` (Lennart, 2026-10-15, not built). house_prices_nominal REVIEW, the same open question |
| 5 | Licence put to the curator | departs from a same-day sibling, no reason given | mortgage panel 2026-10-20 (same terms text): "licence noted (EV-4)", not a curator issue. lgd: in `license` only. EV-4 (Must), lucas_topsoil (2026-09-23, Lennart) |
| 6 | Probe gap | stale: superseded by a rule of 2026-10-12 | task_probes.md, `uniform_within_class` and its calibration of 2026-10-12. CHANGELOG 2026-10-12 |
| 7 | Accepted warning `task_target_low_cardinality` | consistent in outcome; the cited analogy rests on a different fact; this is the third acceptance | wine_quality, numerai_v5_2_1m |

**Details**

**1. OpenML 46372 (issue 1) and the record's `source_links`**

**Already settled.** Lennart decided this on 2026-10-12. The CC on `corporate_credit_rating_cat_data_set_ratings_raitings_duplicate` reads: "No: generated data (AHDS), a simulated copy of the book's rows that corporate_credit_rating_cat_data_set_ratings_raitings curates". `provenance.md` carries the PROV-15 Cases row "OpenML 46372 | a generated table made from the book's 197 rows, posing as real: a problem of that copy". So issue 1 is no open question: the definition follows the decision. The REVIEW can state it as decided rather than ask.

**The fix to the record understates the problem.** The issue names only the first link. The measurements of 2026-10-07 show that two of the four `source_links` are the generated file. The verification output of that run (panel run) gives "polanitz (5000, 8)" with 500 rows per code. So `github.com/Polanitz/.../ratings.csv` is the same simulated table as OpenML 46372, not the book's 197 rows.

The Medium article is related work. records.md says: "Related work goes into the comments, not here".

The precedents point the same way:
- lung_cancer, miami_housing and immoscout_german_house_prices had their OpenML copy links removed (2475ea2, 2026-10-14).
- nyc_taxi_trip_duration and melbourne_housing_market had related links moved out (58ee235, curator's review of 2026-10-20).
- The sibling records lgd and mortgage list only the book's data page.

There is also a de-duplication reason. `source_links` "double as its identity for de-duplication" (records.md). Today the OpenML link sits in both this record and `_duplicate`.

What would follow precedent: `source_links` keeps the data page (and the file URL), and the Medium article and the GitHub CSV go to a comment line. This is a record edit that needs no decision. It can be applied rather than raised.

**2. Target framing (issue 2) and the record's `problem_type`**

**The pair decided the other way.** The closest precedent with the same kind of target is the same curator's credit-rating task. corporate_credit_rating was framed as 6 letter classes: CCC/CC/C merged by the rating convention, AAA (7 rows) and D (1 row) dropped. Lennart's CC of 2026-10-16 on corporate_issuer_credit_rating keeps "Its decision of 6 letter classes (CCC/CC/C merged)" as the starting point. This record's own note, by Lennart, also leans "likely classification … due to ratings being categories officially". The REVIEW cites neither as a precedent.

**Facts that set this case apart** (written in the REVIEW, so the departure has a stated reason):
- There, the letters are known, so a merge follows a field convention (TP-7; audiology_diagnosis "classes merged by a convention of the field, and the merge tested"). Here only "1 = AAA" is given, so any letter merge rests on an unverified mapping.
- 197 rows against 2,029.

**Option (b) is misread against TP-8.** The REVIEW says option (b) "still leaves codes 3 and 9 at 4 rows per test fold, near the parkinsons line", and the issue opens with "Regression is the only framing with neither a Too Small class nor an assumed mapping." Measured on `ratings.csv`, the counts per code are {1: 3, 2: 5, 3: 14, 4: 32, 5: 37, 6: 49, 7: 23, 8: 18, 9: 12, 10: 4}.

- Dropping codes 1, 2 and 10 follows ecoli_proteins (drops omL 5, imL 2, imS 2: "less than 10 samples") and lung_cancer (drops a 6-row class).
- The smallest classes left, 12 and 14 rows at about 4-5 per test fold, fall inside the band Lennart kept on 2026-10-12 under TP-8:
  - forensic_glass_identification: 9 and 13 rows, 3 and 4-5 per fold;
  - ljubljana_primary_tumor: 10 and 14 rows;
  - mic: 12 rows, 4 per fold;
  - sarcoma: 10 rows, 3-4 per fold.
- parkinsons (TP-5, 2026-10-05) was 8 units of a binary class at 2-3 per fold, with `no_spread` and `unstable` flags. It is not the comparable line.

So option (b) has no Too Small class and no assumed mapping. Its cost is different: it truncates the scale, dropping AAA/AA+ and the bottom code. That is a USE-5 question (is it still the target the actor acts on?), not a TP question. The issue should say so.

**For regression.** wine_quality ships a 0-10 grade as regression with rare end grades (grade 9: 5 rows, grade 3: 30). The accepted warning cites it. The fact behind wine_quality is that the paper models regression (Cortez et al. 2009, Sec. 2.2). The fact here is different: the R Companion fits an ordered logit, a classification model, and scores it in notches. The analogy supports the metric (distance matters) more than the model class. This is worth one clause in the warning and in the issue.

**The `problem_type` field.** Listing the field disagreement and leaving it to the curator matches lgd (REVIEW issue 1, record Binary vs definition Regression). The rule (records.md, definitions.md) is that the record follows what ships. A `_clf` second folder is the house route if both framings are wanted (definitions.md; pva_revenue_prediction_kddcup98). It is not mentioned as an option; it could be.

```text
**Consistency check (AI, 2026-10-20):** your call on corporate_credit_rating_cat (regression on the 1-10 code, as
implemented) differs from corporate_credit_rating / corporate_issuer_credit_rating (letter classes, rare grades merged
or dropped; your CC 2026-10-16) and from your note on this record ("likely classification"). What sets it apart?
(a) the code-to-letter mapping is unverified (only "1 = AAA"), so no merge can follow a rating convention, and 197 rows
leave codes 1, 2, 10 at 3-5 rows; recorded as the reason, with wine_quality as the regression precedent;
(b) treat it like corporate_credit_rating: classification, dropping codes 1, 2, 10 as ecoli_proteins does (7 classes,
smallest 12-14 rows, inside the TP-8 band kept on 2026-10-12);
(c) reopen the issuer rebuild's framing to match (a notch regression there too);
(d) write a rule for ordinal targets (when a rating or grade is regression, when classes).
```

**3. Provenance gaps (issue 3)**

**Consistent.** Keeping a dataset whose source is plausible but unclear in detail follows bad_customer_detection (PROV-2, "kept, with a note of what to clarify", Lennart 2026-10-14). The same book's lgd carries the same "modified?" question as an open issue (lgd REVIEW issue 5). The retired textbook siblings fail tests that these rows pass:
- homeq_default_prediction (Lennart, 2026-09-24): near-copy clusters pure in the label, distance AUC 0.92; here the nearest-neighbour code agreement is 25.5% against 22.4%;
- healthcare_insurance_expenses (Lennart, 2026-10-06): a recovered formula; here the `formula` mark gives 0.0% exact.

So "kept with notes" is the precedent outcome.

**Two corrections:**
- **"The book text was not read."** The lgd run of 2026-10-07 read chapter 1 from the publisher's excerpt (`https://www.sas.com/storefront/aux/en/spcriskmdl/68835_excerpt.pdf`). It cited p. 14 ("slightly modified and anonymized") and Exhibit 1.4 (p. 12: each data set filed under a risk segment). (The lgd run's draft issues, 2026-10-07.) This record's own "From the book" quote ("an anonymized data set with corporate ratings … numerically encoded") most likely comes from that chapter. Chapter 1 may settle part of what issue 3 asks chapter 8 for: the segment, perhaps the encoding, and whether the data were modified. Read it before asking Lennart for pp. 213-236, as was done for lgd.
- **"Pass the generated-data probe."** On the 197 rows, only `independent_columns` ran. `uniform_within_class` needs classes of at least 50 rows, and the largest code has 49. task_probes.md (calibration of 2026-10-12) says so for this very table: "no class of 50 rows; with classes down to 10 rows they give 17.1% of 105 pairs dependent and 10 of 24 cells uniform, no flag", and the KS test loses power below 50 rows. The no-flag result is weak evidence (EV-3). The issue should say the within-code test cannot run here, and lean on the direct check it already has: real within-code dependence, mean |rho| 0.21-0.42.

**4. Name (issue 4)**

Keeping the name follows records.md: "Renaming breaks links and review marks, so names stay". The alternative has one precedent: Lennart renamed `churn_telco_nigeria` to `churn_telco_south_asia_duplicate` on 2026-10-15, an unbuilt dataset whose name misdescribed the data. house_prices_nominal has the same open question and its REVIEW says the rename has "no precedent". That is inaccurate, and the two should be decided alike.

A rename here also touches the `_duplicate` record. Its `unique_name` and the text of its CC of 2026-10-12 both name this record.

**5. Licence (issue 5)**

The content is consistent with EV-4 (Must: never a verdict reason) and lucas_topsoil (2026-09-23). The framing departs from the siblings. mortgage, with the same `license` text from the same site, had a full panel on 2026-10-20 and lists the licence as "noted (EV-4)", not as a question to Lennart. lgd, the same terms again, raises no licence issue. If the redistribution question for a public collection matters, it applies to all three book datasets (and to expresso and 2_month_survival_rate_prediction, among others). It belongs in one cross-dataset question, not in this folder alone.

```text
**Consistency check (AI, 2026-10-20):** issue 5 asks you whether the collection may redistribute ratings.csv; mortgage
(panel 2026-10-20) and lgd carry the same Credit Risk Analytics terms and only note them (EV-4). What sets this one
apart? (a) nothing: note it here too and drop the issue; (b) ask once for all three book datasets (a cross-dataset
item); (c) reopen mortgage and lgd with the same question; (d) a house rule on redistribution for public collections.
```

**6. Probe gap (issue 6): stale**

The issue says `generated_probes.py` does not flag the 5,000-row file and proposes a within-class check "per class". That check exists. It is `uniform_within_class`, added on 2026-10-12 (CHANGELOG 2026-10-12: "flags … values drawn uniformly within each class"). Its calibration in task_probes.md reads: "OpenML 46372 has 4.0% of 150 within-class pairs dependent and 60 of 60 cells uniform", and the flag fires on it.

The issue's text predates that change (from the 2026-10-07 run). If the earlier run really gave no flag, then either it ran an older probe or it was run as regression in a way that skipped the mark. That is a probe bug to report, not a rule gap. Either way the issue as written contradicts the knowledge file and should be dropped or rewritten after a re-run.

**7. The accepted check warning (`task_target_low_cardinality`)**

This is the third accepted use of the warning:
- wine_quality: "the paper models it as regression";
- numerai_v5_2_1m: "Numerai treats it as regression";
- this dataset: the source scores in notches.

The first two rest on the source modelling regression. This one rests on a weaker fact (an ordinal model scored by distance). It is not the same reason three times, so no amendment is strictly due under principles.md. Still, no rule says when an ordinal target is regression, and point 2 shows two credit-rating tasks framed differently. A short rule (TP-7 or USE-5, with these cases as Cases rows) would prevent drift.

**Drift and register flags**

- **No drift by the curator on the rules involved.** Lennart's credit-rating calls (2026-10-07 to 2026-10-16) are consistent with each other. The departure in point 2 is the AI's definition, which the curator has not yet decided on.
- **Register flag 1** (`few_minority`, opposite outcomes): alvin is excluded against seven keeps. It bears on point 2 only as the TP-8 band cited above. alvin's windows held 27-41 test rows from 5-12 users, which is not comparable.
- **Checklist numbers.** The off-by-a-digit numbers in the checklist (Spearman -0.385 vs -0.39; ridge 0.283/0.296 vs 0.286/0.299) are procedure (writing.md), not precedent questions.

**Files**

- Definition: `datasets/_dev/tabarena-v0pt2/corporate_credit_rating_cat_data_set_ratings_raitings/dataset.py`
- Record: `curation/records/corporate_credit_rating_cat_data_set_ratings_raitings.md`
- Duplicate record: `curation/records/corporate_credit_rating_cat_data_set_ratings_raitings_duplicate.md`
- Generated-data probe rules: `.claude/skills/knowledge-curation/references/task_probes.md` (lines 222-276)
- Sibling REVIEWs:
  - `datasets/_dev/tabarena-v0pt2/lgd/REVIEW.md`
  - `datasets/_dev/tabarena-v0pt2/mortgage/REVIEW.md`
- Polanitz CSV evidence: the verification output of the 2026-10-07 run (panel run)

</details>

<details><summary>Advocate</summary>

**Advocate: corporate_cat**

Dataset: `datasets/_dev/tabarena-v0pt2/corporate_credit_rating_cat_data_set_ratings_raitings/` (re-check, 2026-10-20). Position: ship as defined, after the note and record fixes listed under point 7.

**1. The definition fixes a problem with the source by going back to its origin (P5; PROV-13 Must, PROV-3 Must, SEL-16 Must)**
- **Evidence.** The claim audit (row 18) found OpenML 46372 generated from the book's rows:
  - All 30,000 of its values lie inside the minimum-to-maximum range of the book's rows with the same code.
  - None of its rows is a book row, and it has exactly 500 rows per code.
  - The ratios barely move together within a code: mean |rho| 0.026-0.042, against 0.21-0.29 in the book's rows.
- **The file we use is the book's own.** `ratings.csv` has the stated sha256. It is identical to the book's `ratings.sas7bdat` (max abs diff 0.0) and to two GitHub copies (claim audit rows 15-16).
- **Precedent.** Lennart's comment of 2026-10-12 on the `_duplicate` record says "No: generated data (AHDS), a simulated copy of the book's rows that corporate_credit_rating_cat... curates". PROV-15 has a Cases row saying the same.
- **Answers the blind reviewer's "provenance does not match".** The clean room's task.md linked the OpenML and GitHub copies, not the book's file. The reviewer found that those copies have 500 rows per class, do not match the 197 rows, and "look resampled or generated". That is our own finding, reached independently. It argues against the copies, not against this definition.
- **Mildest fix.** Edit the record: put the book's data page and file first in `source_links`, and move the Medium article and Polanitz CSV to a comment line, as was done for lung_cancer, miami_housing and nyc_taxi (precedents.md, 1b). This needs no decision.

**2. The 197 rows are real data as far as any test can tell (P5; PROV-3 Must, SEL-16 Must, EV-3 Must)**
- **Evidence.** They pass the tests that retired the same book's other datasets:
  - The nearest neighbour shares the code in 24.8-25.5% of cases, against 22.4-22.8% overall. The closest pair is 0.10 standard units apart (median 0.71). There are no near-copy clusters, unlike homeq_default_prediction, which had a distance AUC of 0.92.
  - No formula reproduces the target (0.0% exact), unlike healthcare_insurance_expenses.
  - The ratios move together within a code (|rho| 0.21-0.29), which the generated copy lost.
- **Concession.** The generated-data probe's "no flag" is weak evidence: `uniform_within_class` needs classes of 50 rows and the largest has 49 (precedents.md, point 3). I rely on the direct within-code dependence instead. Whether the book modified the rows remains untested.
- **Why this outranks the objection.** PROV-3 is a Must, but it needs a finding. A suspicion that the rows were modified, without a test that shows it, is a question (EV-3, EV-7).
- **Precedent and remedy.** bad_customer_detection was kept with a note (Lennart, 2026-10-14), and lgd has the same "modified?" issue left open. The mildest remedy is the existing note, plus reading the chapter 1 excerpt that the lgd run already found (precedents.md, point 3) before asking for chapter 8.

**3. The use case is real and its fit is stated honestly as approximate (P3; USE-1 and USE-8 Must, USE-9 Should)**
- **Evidence.** The practitioner says shadow-rating banks for low-default portfolios is "a real, current practice", and it agrees with `fit="approximate"`. The R Companion's chapter 8 code fits `polr(rating ~ COMMEQTA+...+SIZE)` under "MAPPING TO AN EXTERNAL RATING AGENCY" (claim audit, rows 1-2). USE-9 offers no reframing, because shadow-rating an unrated bank is the use case itself.
- **The gaps are already named.** The definition names the missing statement and rating dates and the unverified scale. USE-8 lists "a label without a stated horizon" as an approximate case (alfa_battle_2_0_task_2).
- **Mildest fix (a note).** Add the practitioner's point to `task_summary.known`: country, sovereign and support inputs are absent, and size partly stands in for support. This is a note, not a change to the task.

**4. The evaluation is honest: no leak, no copies, and the split matches the use case (P4; USE-10 and USE-11 Must, SPLIT-1 Must, LEAK-16 to LEAK-21)**
- **Split.** The split audit says "right with notes". Shadow-rating an unrated bank is a cold start. There is one row per institution (197 unique `spid`), so IID needs no grouping.
- **Alternative splits change nothing beyond noise:**
  - Holding out a file block scores ridge R² 0.262, against 0.255 for a random split of the same size.
  - Holding out a `spid` range costs 0.008-0.024 R², within the per-split SD of about 0.1.
- **No institution is repeated across the blocks.** Cross-block look-alike pairs share the code only 7.5% of the time, and ratings are sticky from year to year.
- **The timing question is not a leak.** No column is shown to come after the rating. The column audit says "question, not a leak"; the practitioner calls it "harmless for a cross-section read as concurrent".
- **Why this does not require exclusion.** LEAK-1 and USE-3 are Musts that are fixed in the definition when they can be. There is no column to drop or lag and no evidence of a leak. The gap is already the stated `fit_reason`, so a note is the right step on the remedy ladder.

**5. Regression on the code is the right framing (P3 and P6; USE-5 Must, TP-5 and TP-7 Must)**
- **Evidence for regression.**
  - As 10 classes, codes 1, 2 and 10 hold 3, 5 and 4 rows, about 1 per test fold. That is `Too Small` under TP-5.
  - The source scores the model by distance: `notchdiff <- abs(as.double(rating) - as.double(prediction))` (claim audit, row 26).
  - The direction 1 = AAA is supported by the data: bigger, more liquid banks and those with lower provisions get better codes (claim audit, row 49).
  - The practitioner says "Regression is the right framing; 10 classes would throw away the order".
- **The alternatives build the target ourselves.**
  - Option (b), dropping codes 1, 2 and 10, cuts AAA/AA+ off the scale. That is a USE-5 problem, as precedents.md itself says.
  - Option (c), letter-grade groups, rests on an unverified mapping of codes to letters.
  - Both are targets we would construct. TP-7 requires an established convention for that, and none exists here. Regression keeps the source's labels unchanged.
- **The objection from precedent.** corporate_credit_rating used letter classes. Two facts set this case apart: there the letters were known, so a merge could follow a field convention, and it had 2,029 rows against 197. wine_quality is the precedent for regression on a grade.
- **Concession.** The equal-step notch reading is unverified, and RMSE assumes it. Keep the existing note. Reword the accepted warning: the source supports a distance-based metric, not a regression model (precedents.md, point 7).

**6. The dataset is worth benchmarking: small but real (P6; TP-5 Must, TP-8 Must, tiny-but-real tension)**
- **Evidence.** Linear models beat the dummy on 100% of splits, with skill +0.319 ± 0.066. Linear beats LightGBM by +0.138 (paired SE 0.015), and ridge R² is 0.283 against 0.227 for a random forest. There are no task-probe flags.
- **Precedent.** principles.md says "a small dataset is a tiny-data task" (musk kept). `Too Small` is for a handful of units per class per fold, which applies only to the classification framing we did not ship.
- **Answers the blind reviewer's "rankings mostly noise".** There are 60 splits, each test fold has 65-66 rows, and a 161-row regression already ships.
- **Concession.** "Ridge beats RF on 75% of splits" is 61.7% when re-measured. Only the direction holds.

**7. The remaining findings are notes and record edits, not reasons to stop shipping (P7, procedure; EV-4 Must, writing.md)**
- **Cleaning.** The column audit found no cleaning problem in any column. Dropping `spid` follows CLEAN-3, and keeping the outlier is checked (a unit slip would fit worse: mean R² 0.283 to 0.266 or 0.248).
- **Fixes to apply now, none of which needs a decision:**
  - Spearman for liquid assets: -0.39 becomes -0.38.
  - State the ridge settings, or round 0.286/0.299 to "about 0.28 to 0.30", and the block AUC to "about 0.5".
  - Record: `problem_type` should follow what ships; "198" becomes 197; the "From the book" quote is from the data page.
  - Drop the stale issue 6: `uniform_within_class` already flags OpenML 46372.
  - Add the costs-to-income shift between the two `spid` ranges to the `spid` bullet.
- **Licence.** Note it, as for mortgage and lgd (EV-4: never a reason for a verdict). If redistribution matters, it is one question for all the book's datasets.
- **Name.** records.md says "names stay". A rename before the first build is the curator's choice, not a reason to block shipping.

**Judgment record (advocate)**
Verdict: ship after changes (notes and record only).
Validity: SEL-16 and PROV-3 hold as far as testable (book file real; generated copy replaced, PROV-13); USE-1 holds, USE-8 approximate (timing, scale, missing country and support named); LEAK-1/USE-3 untested, no column shown to come after the rating, kept with a note; USE-10, USE-11 and SPLIT-1 hold; LEAK-16 to LEAK-21 hold.
Value: TP-5 is not triggered for regression; real signal (linear beats the dummy on 100% of splits).
Quality: CLEAN rules hold; numbers in the notes corrected (procedure).
Weighed: size -, source + (origin file), gap - (country, support, timing), real use +.
For the curator: the framing (regression vs classes, against the corporate_credit_rating precedent) and the name are weighing calls; the licence goes to one cross-dataset question.

Files: the evidence is in the panel's reports (claim_audit.md, column_audit.md, split_audit.md, practitioner.md, precedents.md, blind_review.md, checklist.md). The definition is datasets/_dev/tabarena-v0pt2/corporate_credit_rating_cat_data_set_ratings_raitings/dataset.py and the record is curation/records/corporate_credit_rating_cat_data_set_ratings_raitings.md.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate rebuttal: corporate_cat**

**Facts I checked**

I read the chapter 1 excerpt the critic cites, the publisher's chapter 1 excerpt (https://www.sas.com/storefront/aux/en/spcriskmdl/68835_excerpt.pdf).

- **The quote is in the book.** P. 14 reads: "The ratings data set is an anonymized data set with corporate ratings where the ratings have been numerically encoded (1 = AAA, and so on)".
- **What follows.** The record's "From the book" attribution is correct. Claim audit row 54 ("refuted on attribution") is wrong, and so is "the book text was not read" in REVIEW issue 3 and in the accepted warning. The book gives no agency, period or provider, so the gaps the definition states stand.
- **New fact.** Exhibit 1.4 lists "Ratings | Corporate | 5 | Credit scoring". The book files these rows under its Corporate segment and uses them for chapter 5, credit scoring.
  - The text extraction garbles the chapter column, so whether chapter 8 also uses them cannot be read from it.
  - This bears on point 6 below and on the name.

**Point 1: rating type and scale (P3, USE-5 Must)**

**Concede.** Add "which rating (issuer or other) is not stated" to `fit_reason` and keep the notch caveat.

**Why that is enough, not a stop.** This is not like corporate_credit_rating.
- There, 17% of the labels that could be checked were measurably not the issuer rating. That was a finding.
- Here nothing contradicts a single rating type. The orientation is confirmed (claim audit row 49). Codes 7-10 have bank-like ROE and LLP, which rules out the letter-grade reading.
- USE-5 asks for a finding that the label is wrong, and there is none. The remedy is a note (USE-8, approximate).

**Point 2: the framing against precedent (TP-7 and TP-8 Must; treat like cases alike)**

**Concede three things:**
- REVIEW issue 2 must cite the corporate_credit_rating framing and the record's own "likely classification" note.
- "Near the parkinsons line" is wrong. Option (b) leaves 12-14 rows per class, which sits inside the TP-8 band kept on 2026-10-12.
- The accepted warning should say the source fits an ordered logit and scores it in notches. The wine_quality analogy supports the metric, not the model class.

The consistency check that precedents.md drafted (options a-d) should replace the current issue text.

**Dispute: option (b) is not as good as regression.**
- Dropping codes 1, 2 and 10 means the definition builds the target itself. TP-7 (Must) then requires an established convention for the drop, and there is none here.
- In corporate_credit_rating the letters were known, so CCC/CC/C were merged by the rating convention. The facts that set this case apart are written down: only "1 = AAA" is known, and there are 197 rows against 2,029.
- Option (b) also removes AAA/AA+, the top of the scale the actor acts on (USE-5). The critic's own brief says so.
- Regression ships the source's labels unchanged and scores by distance, as the source does (`notchdiff`). So "neither a Too Small class nor an assumed mapping" is false as worded, but regression is still the only framing that builds no target.
- The ranking does not settle this one. It is a weighing call for the curator, with the facts above.

**Point 3: the prediction point (P4, LEAK-1 / USE-3 Must)**

**Concede.** It cannot be checked. Keep the `fit_reason` note.

**Dispute: making chapter 8 a stated condition before publication.**
- The remedy ladder takes the mildest remedy that resolves the problem. No fix to the definition exists, and no leak was found: no column is shown to come after the rating, and the block holdout gives 0.262 against a 0.255 control.
- Chapter 1 adds no dates, so there is no sign that chapter 8 will.
- Tying release to a book we may not obtain is exclusion by delay, without a Must violation shown.
- "Read chapter 8 if we can get it" belongs in REVIEW.md as a follow-up for the curator, not as a condition.

**Point 4: the evidence that the data is real (P5, PROV-3 / SEL-16 Must)**

**Concede the wording.** Write that `uniform_within_class` cannot run here (no code has 50 rows), and that the case rests on within-code dependence (|rho| 0.21-0.29) and on there being no near-copies. Add the costs/income shift to the `spid` bullet. I made the same concession in my opening point 2.

**Dispute the weight given to "real and simulated data".**
- The phrase (chapter 1) describes the book's data in general. No entry in the excerpt is labelled simulated. That includes HMEQ, which we retired from a measurement on the data (PROV-3 test 5, distance AUC 0.92), not from the text.
- A measurement on the data outranks a page (EV-2). The ratings rows pass the test HMEQ failed: nearest-neighbour code agreement 24.8% against 22.8%, closest pair 0.10 standard units.
- Exhibit 1.4 now ties the rows to a real segment (Corporate) and a modelling chapter.
- The `spid` ranges are a population question, not a generation mark. Holding a range out costs 0.008-0.024 R², within noise (split audit).

**Point 5: the record points to the generated copy (P5, PROV-1 / PROV-8 Must)**

**Concede in full.** This is a repair that needs no decision:
- Make the data page and the file URL the `source_links`.
- Move OpenML 46372, the Medium article and the Polanitz CSV to a comment.
- Correct 198 to 197.
- Align `problem_type` with the framing that ships.

The blind reviewer's report is the evidence that the current links mislead. As I said in my opening point 1, that is a fault of the record, not of the definition.

**Point 6: the fit statement leaves out country and support (P3, USE-8 Must)**

**Concede.** Add to `known` or `fit_reason`: "no country or support input; size partly stands in for support".

**On "corporate" against banks.** The book's Exhibit 1.4 files the rows under "Corporate", and p. 14 says "corporate ratings". The bank reading comes only from the ratio types (claim audit row 43, circumstantial). Write both in the note: the book says corporate, and the ratios are bank ratios. This weakens the case for the rename in REVIEW issue 4; "names stay" (records.md) is the default.

**Point 7: value and numbers (TP-2, EV-8)**

**Concede every correction:**
- Ridge R²: 0.283 / 0.296 at alpha 1, or state the settings.
- Spearman: -0.38.
- Block ROC AUC: 0.43-0.48, plus the Mann-Whitney p 0.049 on the codes.
- 61.7%, not 75%.
- Drop issue 6.
- Issue 5 becomes a note, or one question across the book's datasets (EV-4).

**On value, we agree.** Noisy rankings are a fact for the curator, not a reason to retire (musk; tiny but real).

**Where this leaves the panel**

Both sides recommend shipping after changes. The changes that need no decision are the record repair, the number fixes and the note additions (points 1, 4, 5, 6, 7). Two things go to the curator: the framing (point 2), a weighing call between regression and option (b), and whether to seek chapter 8, which I argue should be a follow-up, not a condition. The mediator should also correct claim audit row 54 and "the book text was not read".

</details>

<details><summary>Critic</summary>

**Critic: corporate_credit_rating_cat_data_set_ratings_raitings (opening brief, 2026-10-20)**

**Position: ship only after changes.** I do not ask for exclusion. No Must is broken in a way that a fix or a note
cannot handle. But the definition and REVIEW.md claim more certainty than the evidence gives. The record still points
to the generated copy. And one framing call departs from the curator's own credit-rating precedent without saying so.

**New fact for the panel.** The publisher's chapter 1 excerpt
(https://www.sas.com/storefront/aux/en/spcriskmdl/68835_excerpt.pdf), read in the lgd run, says on p. 14: "The
ratings data set is an anonymized data set with corporate ratings where the ratings have been numerically encoded
(1 = AAA, and so on)". It names no agency, years, country or origin. The LGD entry on the same page, by contrast, says
"provided by a European bank ... slightly modified". Two statements are therefore wrong: "the book text was not read"
(REVIEW issue 3), and the claim audit's row 54, "refuted on attribution". The record's "From the book" quote is in the
book.

**1. P3, USE-5 (Must): what the target is, and its scale, is not established**

- **Problem.** The target is regression on the code, scored with RMSE. RMSE treats every step as one equal notch. The
  only sources (the data page and ch. 1, p. 14) say "1 = AAA, and so on". So whether a step is a notch or a letter
  grade is unverified (claim audit 39, untested). Which rating it is (the issuer rating, the stand-alone profile, or a
  debt rating) is not stated anywhere.
- **Why it matters.** USE-5 retired corporate_credit_rating because 17% of its labels were not the issuer rating. The
  pattern under USE-5 is "a credit rating → the issuer rating". Here we cannot check that at all. The practitioner
  reads the equity sign (+0.26 with a worse code) and size as the strongest predictor (-0.50) as signs of a
  supported issuer rating. That is plausible, but it is an inference.
- **What the data shows.** The data favour notches: codes 7-9 have median ROE of 8-11%, and code 10 has median ROE
  2.8% and LLP 1.1%. That is supporting evidence, not proof (EV-7).
- **Remedy (a note, not exclusion; PROV-2 allows a plausible but unclear detail).**
  - Add to `fit_reason`: "which rating (issuer or other) is not stated".
  - Keep the notch caveat.
  - Get chapter 8 (pp. 213-236) before the collection is published.

**2. P3/P6, consistency (principles.md, "Treat like cases alike"; TP-7, TP-8 Must): the framing departs from precedent and REVIEW issue 2 misstates the alternative**

- **Problem.** The curator framed corporate_credit_rating as letter classes, merging the rare grades and dropping
  others (CC 2026-10-16, carried into corporate_issuer_credit_rating). This record's own note leans "likely
  classification". REVIEW issue 2 cites neither.
- **Option (b) is misread.** The issue says option (b) leaves codes 3 and 9 "near the parkinsons line". In fact,
  dropping codes 1, 2 and 10 leaves classes of 12-14 rows at 4-5 per fold. That is inside the TP-8 band the curator
  kept on 2026-10-12 (forensic_glass, ljubljana, mic, sarcoma; precedents.md, point 2). So "the only framing with
  neither a Too Small class nor an assumed mapping" is false.
- **The cost of (b) is elsewhere.** It truncates the scale, which is a USE-5 question.
- **The wine_quality analogy is weaker than the warning says.** wine_quality rests on the paper modelling regression.
  Here the source fits an ordered logit and only scores it in notches.
- **Remedy.**
  - Rewrite issue 2 with the consistency check that precedents.md drafted (options a-d).
  - Add one clause to the accepted warning: the source's model is an ordinal classifier.

**3. P4, LEAK-1 / USE-3 (Must): the prediction point cannot be checked**

- **Problem.** No source dates the statements against the ratings. If the ratios come from the rating year or later,
  ROE and costs/income can carry effects of the rating (column audit, problem 1).
- **What the data shows.** No probe can settle this. The block holdout, the only proxy for a period, shows no shift
  (0.262 against 0.255; split audit).
- **Remedy.** Keep the existing `fit_reason` note. Make settling it from chapter 8 a stated condition in REVIEW.md,
  together with point 1.

**4. P5, PROV-3 / SEL-16 (Must): the evidence that the data is real is weaker than written**

- **Overstated claims.**
  - REVIEW issue 3 says the rows "pass the checks that caught HMEQ".
  - The checklist says "Real data: the 197 rows pass the generated-data probe".
  - But `uniform_within_class`, the test that catches this kind of generation, cannot run here: it needs classes of at
    least 50 rows, and the largest code has 49 (task_probes.md calibration; precedents.md, point 3). The no-flag
    result is weak evidence (EV-3).
- **Context.**
  - The same book retired HMEQ as generated.
  - The book's site offers "real and simulated data" (ch. 1).
  - Unlike LGD, the ratings entry names no data provider.
  - The two `spid` ranges differ in mean code (p 0.001), and within a code on costs/income (p 0.004; column audit).
    That points to two populations or two vendors, which nobody has explained.
- **What does support real data.** Within-code |rho| is 0.21-0.29, and there are no near-copies (claim audit; split
  audit).
- **Remedy (a note).**
  - Rewrite the wording to say the within-code uniformity test cannot run, and that the case rests on within-code
    dependence.
  - Add the costs/income shift to the `spid` bullet.

**5. P5, PROV-1 / PROV-8 (Must): the record points to the generated copy, and that misleads readers**

- **Problem.** Two of the record's four `source_links` are the generated 5,000-row table, and they come first:
  OpenML 46372 and the Polanitz GitHub csv (the 2026-10-07 run's verification output; precedents.md, point 1).
- **Evidence that this misleads.** The blind reviewer followed those links. It found 5,000 balanced rows that do not
  match ours, and recommended exclusion for "provenance does not match" (blind_review.md, concern 1). That is direct
  evidence of the effect.
- **Other errors in the record.**
  - It says "198" rows; the file has 197.
  - Its `problem_type` is Multiclass Classification; the definition ships regression.
- **Remedy (a repair that needs no decision; follows lung_cancer, miami_housing, nyc_taxi).**
  - Make the data page and the file URL the `source_links`.
  - Move OpenML 46372, the Medium article and the GitHub csv to a comment.
  - Correct 198 to 197.
  - Align `problem_type` with the curator's framing.

**6. P3, USE-8 (Must): the fit statement leaves out the largest gaps**

- **Problem.** The practitioner ranks the missing country (sovereign anchor) and the missing support inputs as the two
  gaps that change the task most. Size partly stands in for support. `task_summary.known` and `fit_reason` mention
  neither.
- **Also.** The record and the name still say "corporate", but the data are bank ratios.
- **Remedy (a note).**
  - Add to `fit_reason` or `known`: "no country or support input; size partly stands in for support".
  - Keep the rename as the curator's issue 4.

**7. P6 and procedure (TP-2 Should, EV-7 Must, EV-8 Should): value is thin, and several stated numbers are wrong**

This point is about value and procedure, so it is no reason to exclude.

- **Value.**
  - Codes 1, 2 and 10 are 6% of the test rows but carry 29% of ridge's squared error.
  - The per-split R² has an SD of 0.097.
  - Ridge beats the random forest on 61.7% of splits (paired SE 0.015), not "75%" (claim audit 63b).
  - Method rankings will be noisy. That is a fact for the curator, not a retirement reason (TP-2, musk).
- **Numbers that do not reproduce or are not sourced.**
  - Ridge R² 0.286 / 0.299: it is 0.283 / 0.296 at alpha 1.
  - Spearman -0.39: it is -0.385.
  - "A random forest cannot tell the blocks apart (ROC AUC 0.52)": re-measured at 0.43-0.48, and the codes differ a
    little between the blocks (Mann-Whitney p 0.049).
- **Stale REVIEW issues.**
  - Issue 6 (probe gap): the current probe flags OpenML 46372.
  - Issue 5 (licence): raised as a curator question here, but only noted for mortgage and lgd under the same terms
    (EV-4; precedents.md, point 5).
- **Remedy.**
  - State the model and settings with each number, or round them.
  - Fix -0.38 in `_decisions`, curation_comments and REVIEW.
  - Drop issue 6.
  - Turn issue 5 into a note, or into one cross-dataset question.

**What I ask for, in short**

- **Fix before shipping.** The record repair (point 5), and the text and number fixes in `dataset.py` and REVIEW.md
  (points 4 and 7).
- **Note additions.**
  - In `fit_reason`, the rating type and the missing country/support (points 1 and 6).
  - REVIEW issue 2 rewritten as a consistency check (point 2).
- **For the curator.** The framing (point 2), and whether chapter 8 must be read before the public release
  (points 1 and 3).

</details>

<details><summary>Critic rebuttal</summary>

**Critic: rebuttal to the advocate (2026-10-20)**

We now agree on the verdict: ship after changes, with no exclusion. Two disputes are left, one about a fact and one
about scope. Everything else I concede.

**Conceded**

- **Point 1 (PROV-13).** The book's file is the repair, and the blind reviewer's finding is about the copies the clean
  room linked to. The record edit is the same one I ask for in my point 5.
- **Point 3 (USE-8).** The country and support note goes into `known`. This settles my point 6.
- **Point 4 (P4).** I agree there is no leak, no copy across the split, and that IID is right. The timing question
  stays as a note (LEAK-1 / USE-3). I add only that "harmless if concurrent" is a reading, not a test result (EV-7).
- **Point 6 (P6).** The dataset is small but real, and TP-5 is not triggered for regression (TP-2, musk). One thing
  remains, and it is a note: codes 1, 2 and 10 are 6% of the test rows but carry 29% of the squared error. The
  argument "a 161-row regression already ships" does not address that share, so REVIEW.md should state it.
- **Point 7 (licence, name, number fixes).** The licence becomes a note (EV-4) and the name stays with the curator.
  The number fixes match my point 7.
- **Point 2 (part).** The advocate concedes that the probe gives no real evidence of real data, which was my point 4.
  The remaining facts about modification, and the costs/income shift between the `spid` ranges, become notes.

**Disputed**

**A. Advocate point 7: "the 'From the book' quote is from the data page" (a fact; EV-2, EV-7).**
- This is wrong. The book's chapter 1, p. 14, carries the same sentence: "The ratings data set is an anonymized data
  set with corporate ratings where the ratings have been numerically encoded (1 = AAA, and so on)". The source is
  the publisher's chapter 1 excerpt (https://www.sas.com/storefront/aux/en/spcriskmdl/68835_excerpt.pdf), p. 14.
- So the record's attribution is correct and should not be edited. The definition's "the book text was not read"
  (accepted warning) and REVIEW issue 3 must be corrected instead.
- **On advocate point 2 ("read the chapter 1 excerpt before asking for chapter 8").** It has now been read. It adds
  no agency, years, country or provider. That contrasts with LGD on the same page ("provided by a European bank ...
  slightly modified"). So chapter 1 settles nothing on realness or the scale, and chapter 8 remains the only source
  that can (PROV-2 note).

**B. Advocate point 5: the framing. The advocate's evidence is right; the remedy is incomplete (USE-5 Must; principles.md, "Treat like cases alike").**
- **I accept:**
  - 10 classes would be Too Small (TP-5).
  - Option (b) cuts off the top of the scale, which is a USE-5 cost.
  - The warning gets reworded.
- **Two things the advocate's remedy misses:**
  - **REVIEW issue 2 still has to be rewritten.** As written it says option (b) leaves classes "near the parkinsons
    line" and that regression is "the only framing" without a Too Small class. Both are false under the TP-8 band
    the curator kept on 2026-10-12 (12-14 rows, 4-5 per fold). The departure from corporate_credit_rating has to be
    put to the curator as a consistency check (principles.md, case 2). The advocate itself lists the framing as "for
    the curator", so this is a change to the text, not a new decision.
  - **USE-5 asks which rating the label is, not only its scale.** This is my point 1. The issuer-versus-other
    question is what retired corporate_credit_rating, and neither the data page nor chapter 1 names it. The advocate's
    notes cover timing, scale, country and support, but not this. I ask for one clause in `fit_reason`: "which
    rating (issuer or other) is not stated".

**What remains for the mediator**

- **Changes that need no decision.** The advocate's list of edits, plus:
  - The record's "From the book" attribution stays as it is.
  - Correct "book text was not read".
  - Add the clause about which rating it is.
  - Add the 29% error share to REVIEW.md.
  - Rewrite REVIEW issue 2 as a consistency check.
- **For the curator.** The framing, and whether chapter 8 must be read before the public release.

</details>
