---
unique_name: brilliant_earth_diamond_prices
name: 'Brilliant Diamonds: natural and lab-created diamonds scraped from brilliantearth.com'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Kaggle
year: '2020'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/miguelcorraljr/brilliant-diamonds
- https://github.com/corralm/DiamondScraper
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a dated 2020 scrape of about 119K diamonds listed by one retailer with the 4 Cs, the grading lab and natural or lab-grown, the same task as `diamonds` (shipped) with twice the rows and newer prices.
- Source: Miguel Corral Jr., "Brilliant Diamonds" on Kaggle (miguelcorraljr/brilliant-diamonds, created 2020-12-14, CC BY-NC 4.0), scraped from brilliantearth.com with his DiamondScraper (https://github.com/corralm/DiamondScraper); Kaggle is the first publication (PROV-8): "this dataset of ~119K natural and lab-created diamonds from brilliantearth.com to demystify the value of the 4 Cs". As published: one CSV with id, url, shape, price (USD), carat, cut, color, clarity, report (grading lab), type (natural or lab created), date_fetched; rows not counted.
- Use case: a buyer or reseller values a stone from its grading before buying or listing it; fit approximate: the target is one retailer's asking price, not a sale price. Regime IID: one scrape over a few days, one row per stone.
- Siblings and duplicates: `diamonds` (`Yes`, the ggplot2 set, 53,940 stones of about 2008, RMSLE on the dollar price per CC 2026-10-21) and `diamonds_duplicate`; another source, so not a duplicate (PROV-4). External collections: none found.
- Better data: from the run's search, found as better data for `diamonds`; no further search this round.
- Papers and pages: the Kaggle page and the scraper repository; no paper.
- Metric: none found (a Kaggle dataset without a task); fallback `rmse`, or RMSLE on the dollar price following `diamonds` (CC 2026-10-21, Lennart: "a price's error matters relative to the price") (MET-1, MET-3).
- Risks for /add-dataset: `id` and `url` are identifiers; lab-grown and natural stones price on different scales (type as a feature or a filter, USE-5); a retailer's list prices may follow a grid on the 4 Cs, which would make the task near-deterministic (TP-4, check); no depth, table or x/y/z measurements as in `diamonds`; repeated listings of a stone (check `id`).
- Priority: gap 0 (business & marketing and regression are not thin), use case 0 (the uploader's motive, no actor's decision), source 0 (an individual's scrape with code, documented only by a column table), shape + (about 119K stones, categorical and numeric), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `diamonds`.
- as published: Diamonds listed for sale, '~119K natural and lab-created diamonds' (description), one CSV of 16.8 MB; columns id, url, shape, price, carat, cut, color, clarity, report (grading lab), type (natural / ...; target: price (US dollars); access: open.
- Why: Same target and features of the same kind as diamonds (a retailer's listing scrape with the 4 Cs and the price), with the scrape date and the scraper published.
- Adds: About twice the rows (119K against 53,940), 2020 prices instead of about 2008, lab-grown stones and the grading lab as features, a dated, reproducible scrape. Lacks the ggplot2 set's depth, table and x/y/z measurements. Licence CC BY-NC 4.0. Not taken: the 'largest diamond dataset' upload (hrokrin, 2023, over 200K ...
