---
unique_name: flavors_of_cacao_ratings_2026
name: Flavors of Cacao chocolate bar ratings database (maintained by Brady Brelinski)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
original_source: Website
problem_type: Regression
original_data_state: One Table
source_links:
- https://flavorsofcacao.com/chocolate_database.html
- https://flavorsofcacao.com/index.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: the rater's own, maintained database behind `chocolate_bar_ratings` (2,841 bars to 2026 against 1,795 in the 2017 Kaggle copy); the curator's doubt on that record (no real task) applies unchanged.
- Source: Flavors of Cacao, "FoC Content by: Brady Brelinski © 2011-2026", https://flavorsofcacao.com/chocolate_database.html, a sortable table loaded from `database_w_REF.html` ("Updated on: April 19, 2026"). As published (table previewed 2026-10-31): 2,841 rated bars x 10 columns: REF (a review batch number, 708 values), Company (Manufacturer), Company Location, Review Date (2006-2026), Country of Bean Origin, Specific Bean Origin or Bar Name, Cocoa Percent, Ingredients (count and codes, such as "3- B,S,C"), Most Memorable Characteristics (short tasting notes), Rating (1 to 4 in steps of 0.25; 3.0 to 3.5 for 62% of bars).
- Rating: one reviewer, one bar from one batch, judged on flavor, texture, aftermelt and overall opinion; "4.0 - 5.0 = Outstanding" down to "1.0 - 1.9 = Unpleasant" (https://flavorsofcacao.com/review_guide.html).
- Use case: none clear; at most a buyer or retailer predicting one critic's rating of a new bar from its maker, origin, cocoa share and ingredients; the curator on the parent: "This seems not to make much sense as a real predictive task". Regime temporal by review date.
- Siblings and duplicates: `chocolate_bar_ratings` (Lennart `TBD -> 2nd Tier`, `No Good Target / Scientific Discovery`; the Kaggle rtatman upload of 2017, in CARTE/TARTE, MulTaBench and STRABLE): a version of this source (PROV-6), this one newer and larger; the curator decides which enters. External collections: the parent's collections hold the 2017 copy.
- Better data: found as better data for `chocolate_bar_ratings`; no further search this round.
- Papers and pages: the site's database and review guide; the benchmarks named on the parent used the 2017 copy.
- Metric: none found (a review site), so the fallback `rmse` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: "Most Memorable Characteristics" is written with the rating by the same reviewer ("chewy, off, rubbery" with a 3) (LEAK, USE-3); REF is a batch number that grows with time; the target is one person's taste (USE-2); short text columns.
- Priority: gap 0, use case 0 (none), source 0 (a personal site; a review guide, no data documentation), shape + (2,841 bars, mixed, temporal), risk - (the tasting notes, the curator's target doubt).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `chocolate_bar_ratings`.
- as published: Rated bars, about 2,700 (from the page's banner 'database_2700_bars'; not counted); columns REF, Company (Manufacturer), Company Location, Review Date, Country of Bean Origin, Specific Bean Origin ...; target: Rating (1-5 scale); access: open.
- Why: The publisher's maintained version of the record's source (Kaggle rtatman upload of 2017).
- Adds: About 900 more bars (2,700 against 1,795) and reviews up to 2026, plus the ingredients and tasting-note columns added after 2017. A version of the same source (PROV-6); it does not settle the record's 'No Good Target' doubt.
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
