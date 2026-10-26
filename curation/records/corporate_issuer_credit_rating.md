---
unique_name: corporate_issuer_credit_rating
name: Corporate issuer credit ratings (SEC rating histories and EDGAR statements)
tags:
- Non-IID (Temporal)
original_source: GOV Website
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://ratingshistory.info/
- https://www.sec.gov/structureddata/rocr-publication-guide.html
- https://www.law.cornell.edu/cfr/text/17/240.17g-7
- https://www.sec.gov/edgar/sec-api-documentation
needs_review:
- suggestion
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-10-16, Lennart): new record to rebuild `corporate_credit_rating` from the original sources, after that record was retired for its build (a bond's or loan's rating as the label in 17% of the checkable rows, Moody's grades and delisted companies dropped). Its decision of 6 letter classes (CCC/CC/C merged) is the starting point.

**Assessment (AI, 2026-10-16):** what a rebuild needs; the verdict is the curator's.
- Ratings: every registered agency must publish its rating history under SEC Rule 17g-7(b) (issuer and instrument ratings, action class new / upgrade / downgrade / withdrawal, LEI or CIK, CUSIP). ratingshistory.info converts the files to CSV, no login: Moody's 2012-06 to 2023-12, Fitch 2012-06 to 2025-09, Egan-Jones 2011-01 to 2025-10, DBRS 2012-06 to 2023-11. S&P (2010 to 2021-07) only from an archived copy of that site's CSV; S&P's own page refused scripts. The histories start with a snapshot of the ratings outstanding on 2012-06-15 (action code `HS`).
- Label: the issuer rating, by agency: S&P issuer credit rating (local currency, long term), Moody's Corporate Family Rating (else long-term issuer rating), Fitch long-term Issuer Default Rating, Egan-Jones obligor long-term rating. Notches are available.
- Features: annual statements from SEC EDGAR XBRL (companyfacts), each fact with its filing date, so a row uses only statements filed before its date; delisted filers are included. 24 of the old 25 ratios come from the statements; EV/EBITDA needs share prices. Sector from the SIC code.
- Proposed task (rating migration): one row per issuer, agency and annual statement; features from the statement and the agency's issuer rating in force when it was filed (missing for a new issuer); target the issuer rating in force 12 months later; temporal split. Agencies differ in what they list (S&P and Egan-Jones include affirmations, Moody's only changes), which this framing does not depend on.
- Matching: CIK where the files give one, else names against EDGAR (Egan-Jones has no LEI or CIK). A lower-bound name match finds about 1,200 S&P, 900 Moody's and 1,400 Egan-Jones issuers (the old file: 593 companies).
- Needs: an organisation name and contact address for the SEC's User-Agent (its bulk files refuse requests without one). Effort: about 1.5-2.5 weeks of agent work; matching issuers to filers is the main risk.
- Licence: the agencies' terms for redistributing their histories are not checked (a note, not a verdict reason).
- Previous version: `corporate_credit_rating` (Kaggle agewerc/corporate-credit-rating, 2,029 rows), definition in git at commit 2475ea2.
