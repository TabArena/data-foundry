---
unique_name: book_price_prediction
name: BOOK_PRICE_PREDICTION
checked_by:
- Lennart
- Mustafa
- Myunghwan
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target (yet)
tags:
- Free Text (Sentences)
- New IID
collections:
- TabSTAR
- AutoML_MM
- MulTaBench
original_source: Website
year: '2019'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://machinehack.com/hackathons/predict_the_price_of_books
- https://www.openml.org/search?type=data&id=46663
source_row: 595
type_adapter_id: curation-record-v1
---

## Comments

Book Price Prediction

Unclear how much price can be predicted and depends on the features, needs to be investigated. Plus unclear if text helps. Maybe price needs inflation adjustment? Could get more data from the internet for this? Unclear if it is a real task but was used as such in a competition.

has titles, authors, edition, genre, and category as entities but synopsis as sentences of free text

CC (2026-10-19, Myunghwan): Hold before adding book_price_prediction to TabArena. Approved the summary of findings and inconclusive points, and requested preserving this as an example of curator-directed non-standard checking. This is deferral, not a rejection as trivial, artificial or definitively leaky.

**Assessment (AI, 2026-10-29):** Preserve the earlier approved hold, previously saved only in a local practice record. Useful price signal survives the tested deduplication, while repetition contributes to performance: on identical held-out rows, removing matching training records reduces TF-IDF log-price R2 from about0.440 to0.390, versus0.441 after removing the same number of arbitrary training records. There are203rows with identical recorded predictors but different prices. Different editions can legitimately differ, but edition-aware keys do not explain the remaining repetitions; observation dates, seller IDs and ISBNs are absent. Neither retaining every row nor selecting one per edition therefore has a supported sampling interpretation. TF-IDF/SVD versus MiniLM differs by about0.024R2 after the tested deduplication, but the conditional uncertainty allows a difference of about0.042, leaving representation sensitivity inconclusive. These are bounded diagnostic comparisons, not a universal text-modality verdict or a new cutoff. No artificial-price mechanism was established; a review-count parsing bug is repairable. Price/currency meaning and the observation/split policy remain unresolved. Retain TBD -> Yes with DF: Suspended; reopen only with stronger collection/observation identity evidence or a specifically authorized check resolving the uncertainty, followed by curator reconsideration. No definition, data cleaning policy or build is accepted.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `amazon_book_prices_2023` (TBD -> 2nd Tier, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-04, Lennart): `TBD -> 2nd Tier`, priority 1, keeping `No Good Target (yet)`: "let us mark it as 2nd tier for now and move one, this is too unclear for now" (PR #33 review).

**Assessment (AI, 2026-11-04):** re-screen. MachineHack names no site, currency or date; the data are Amazon.in offers in rupees (25 to 14,100, median 373), crawled around October 2019, the offer at crawl time rather than a list price. The closest actor is a seller listing a copy on an existing product page (approximate fit: Amazon's and third-party offers mixed; USE-5, USE-8); a publisher pricing a new title does not fit, since the stars and review count exist only after sales (LEAK-10). 6,237 labelled rows; the review count is missing on 16.7% because the OpenML parser cannot read "1 customer review". The 203 conflicting rows are re-crawls: 1,190 rows are 559 books crawled again, so a split must group by title and author (15.3% of random test rows have their book in training; copying its price gives R² 0.918 there). Log-price R², random / grouped: text ridge 0.398 / 0.370, LightGBM without text 0.404 / 0.382, both 0.505 / 0.479. Metric RMSLE (the archived evaluation page). `mercari_price_suggestion` covers marketplace pricing with a named actor; `amazon_book_prices_2023` is the same kind of price at a larger scale.

## Reference

Machinehack
