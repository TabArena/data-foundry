---
unique_name: goodreads_computer_books
name: Goodreads-Computer-Books
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Out-of-scope Task (CTR/RecSys/Ranking)
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
year: '2021'
domain: Other
required_split:
- Random (IID)
problem_type: Other
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/muneeralhajri/goodreadscomputerbooks
- '# not this dataset: the general Goodreads API books scrape (jealousleopard, 2019-2020), linked here before 2026-10-22'
- https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks
source_row: 813
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the `No` (TabArena workbook reject; the CC asks "what to predict here?") holds: a scraped book listing with no predictive target the source names (SEL-3), close to `books_goodreads` (`No`). One correction: the old link was another dataset; the record's name and year match `muneeralhajri/goodreadscomputerbooks`, now first in `source_links`. The curator has the call.
- Source: Kaggle `muneeralhajri/goodreadscomputerbooks` ("Goodreads-Computer-Books"), uploaded 2021-01-29, CC0; collected from the Goodreads "Computer" category ("This data was entirely scraped via the Webdriver"); as published: one file `Book_Dataset.csv` (146 KB); the card: "The missing values are imputed in this data by the creator" (method not stated). The old link, `jealousleopard/goodreadsbooks`, is the general Goodreads API scrape of 2019-2020 (`books.csv`, 1.6 MB).
- Use case: none from the source ("find out what book you should be reading next", a recommendation idea, SEL-9); a rating would be the only numeric target, with no actor or moment; regime IID.
- Siblings and duplicates: `books_goodreads` (Lennart, Mustafa: `No`, `No Good Target  / Scientific Discovery`, crawled data without a real task); `book_price_prediction` not compared. External collections: none found.
- Metric: none (no task).
- Risks: imputation by the uploader with an unknown method (PROV-3, PROV-13); scraped Goodreads ratings.
- Priority: none (verdict `No`).

Goodreads computer-books metadata table, already in TabArena Reject. The curation comment notes it is a book-recommendation toy task built from crawled metadata with no user-id (not personalizable) and no clear predictive target. It is recommendation-flavored / scientific-discovery crawled data without a genuine predictive label, so it fails the real-predictive-task and representativeness criteria. No.

---

CC: "Book recommendation task based on metadata (no user-id, so not personalizable). Is rather a toy task using crawled data, but might still be usable; unclear predictive task, what to predict here?"

## Reference

Kaggle
