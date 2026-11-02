---
unique_name: corporate_credit_rating_cat_data_set_ratings_raitings
name: CORPORATE_CREDIT_RATING_CAT Data Set Ratings Raitings
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Missing source information
- Not Representative
tags:
- Tiny Data
collections:
- TabSTAR
original_source: Website
year: '2016'
domain: finance
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=46372
- https://medium.com/@polanitzer/multiclass-classification-for-corporate-credit-ratings-using-credit-risk-analytics-book-by-harald-98d5940c745a
- https://github.com/Polanitz/Multiclass-Classification-for-Corporate-Credit-Ratings/blob/main/ratings.csv
- http://www.creditriskanalytics.net/datasets-private2.html
source_row: 786
type_adapter_id: curation-record-v1
---

## Comments

"This dataset is derived from the Credit Risk Analytics book by Harald, Daniel, and Bart, as described in the Medium article by Roi Polanitzer"
From the book:
"The ratings data set is an anonymized data set with corporate ratings where the ratings
have been numerically encoded"?

Version from OpenML has 5k samples (so likely modified). Original has 198
It was likely modified by the Medium author (without saying it anywhere, wow!)

Unclear if a regression or classification task, likely classification (even if it is ordinal classification) due to ratings being categories officially

**Assessment (AI, 2026-10-07):** OpenML 46372 (5,000 rows, 500 per rating) is simulated from the book's `ratings.csv` (197 rows). Each ratio is drawn uniformly between the minimum and maximum of the book's rows with the same rating: all values fall inside, class means sit at the midpoints, and within-rating correlations are 0.03-0.04 against 0.21-0.42. OpenML labels 1 "very_bad", while the book says "1 = AAA". Use http://www.creditriskanalytics.net/uploads/1/9/5/1/19511601/ratings.csv. The ratios are bank ratios. The R Companion's chapter 8 code scores an ordered logit in notches. As 10 classes, codes 1, 2 and 10 hold 3, 5 and 4 rows, so the v2 definition uses regression. Terms: textbook use only, no commercial use, no redistribution (datasets.html, terms.html).

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source -, shape -, risk - (Issue 3: rating scale (notch vs letter) unverified; possible undocumented modification). 197 anonymised bank ratings with six ratios; tiny and thinly documented, though it replaces a generated OpenML copy.

**Correction (AI, 2026-10-20):** the book's `ratings.csv` has 197 rows, not 198 as in the note above (198 lines with the header).

**Assessment (AI, 2026-10-20):** review panel: ship after changes. The book's chapter 1 (p. 14, Exhibit 1.4) holds the quote above and files the data under its Corporate segment, but names no agency, period, country or provider; the ratios are bank ratios. The definition's notes and fit state the rating type, the timing, the scale and the missing country and support inputs. Open for the curator: regression on the code or 7 classes without codes 1, 2 and 10, a consistency check against corporate_credit_rating (issue 2); chapter 8 as a follow-up or a condition (issue 3); the name (issue 4). Record fields for the curator's marks: `source_links` (OpenML 46372 and the Polanitz CSV, the generated 5,000 rows, and the Medium article to a comment line) and `problem_type` (after issue 2). Priority 1: gap - (no thin domain, problem type or regime), use case - (written by the curation; fit approximate), source + (the book's data page and chapter 1 document the encoding and the six ratios), shape - (197 institutions, 6 numeric features, IID), risk - (unclear target scale and rating type, prediction point unverifiable, issues 2-3).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: stand_in mae — the source (R Companion, Ch08_LowDefaultPortfolios.R lines 62-80) tabulates the absolute notch difference |rating - predicted| per error band, not one scalar; MAE is its mean. Scored metric changes from rmse; needs a rebuild to reach the container.

CC (2026-10-21, Lennart): MAE accepted as the stand-in for the book's table of absolute notch differences (over the rmse fallback).

CC (2026-10-26, Lennart): don't ship: "I feel the data and its source is too constructed and too risky to add. There is likely a better real use case somewhere behind this data and this might not be here. ... I am rather on the side to say no about it very clearly going forward."

**Assessment (AI, 2026-10-26):** asked whether any good reason to keep it remains: no. For it stood only that the rows are the book's own (not the generated OpenML 46372) and that the ratios move together as real accounts do. Against it: 197 institutions with six ratios; no agency, period, country, rating type or provider (PROV-2, the book names none and chapter 8 was never obtained); a small signal (ridge R² about 0.28); the end codes too rare to score (codes 1, 2 and 10 hold 12 rows); a textbook licence without redistribution. corporate_issuer_credit_rating, rebuilt from the agencies' own rating histories, covers the task with a real source. `No` + `Missing source information`, `Not Representative`; the folder left the working copy (in git history before this change).

## Reference

@book{baesens2016credit,
  title={Credit risk analytics: Measurement techniques, applications, and examples in SAS},
  author={Baesens, Bart and Roesch, Daniel and Scheule, Harald},
  year={2016},
  publisher={John Wiley \& Sons}
}
