---
unique_name: zomato_bangalore_restaurants
name: Zomato Bangalore Restaurants
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Kaggle
year: '2019'
domain: business & marketing
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants
- https://huggingface.co/datasets/multabench/core-text-reg-zomato-restaurants
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-01):** `TBD -> 2nd Tier`, priority 2: a 2019 scrape of Zomato's Bangalore listings, with the aggregate user rating as MulTaBench's target; real data whose page names an actor (a new restaurant choosing its concept and place), but a crowd rating of established restaurants is the kind of target the curators keep as 2nd Tier (`yelp`, `letterboxd_movie_rating`), and the review text and vote count shipped with it are built from the same ratings.
- Source: Kaggle "Zomato Bangalore Restaurants" by Himanshu Poddar (first upload 2019, one file `zomato.csv`): "The data is accurate to that available on the zomato website until 15 March 2019", scraped in two phases for each neighbourhood and listing category ("Buffet, Cafes, Delivery, Desserts, Dine-out, Drinks & nightlife, Pubs and bars"); 17 columns (url, address, name, online_order, book_table, rate, votes, phone, location, rest_type, dish_liked, cuisines, approx_cost(for two people), reviews_list, menu_item, listed_in(type), listed_in(city)); a codebook on the uploader's GitHub (poddarhimanshu/Coursera_Capstone, "Data Scraping/Documentation.pdf"). As used by MulTaBench (https://huggingface.co/datasets/multabench/core-text-reg-zomato-restaurants): 41,665 rows, target `rate` as a number, the other columns kept except `url`.
- Use case: the page says the data "will help new restaurants in deciding their theme, menus, cuisine, cost etc for a particular location" and that its reviews "will help in finding overall rating for the place". A restaurateur estimating the rating a planned restaurant would earn from its place, type, cuisines and price makes a decision; the rows are established restaurants whose rating has formed, so fit approximate. Regime grouped: a restaurant appears once per listing category and neighbourhood it is listed under, and chains share a name, so the rows of one restaurant (name and address) share a fold.
- Siblings and duplicates: `zomato` (Lennart, `TBD -> 2nd Tier`, `AHDS` and `No Good Target / Scientific Discovery`) links a different upload, Kaggle anas123siddiqui/zomato-database (2023, five tables of a delivery app whose "Credentials like users name, email, password, and sales ... are generated"), so no duplicate by provenance (PROV-4); whether CARTE's and TexTabBench's "Zomato" (that record's collections) is this Bangalore scrape was not checked. Rating precedents: `yelp` (Lennart, `TBD -> 2nd Tier`, `No Good Target (yet)`), `michelin` (`No`), `letterboxd_movie_rating` (`TBD -> 2nd Tier`, priority 1). External collections: MulTaBench (core text-tabular, "Zomato Restaurants").
- Better data: a candidate of the benchmark MulTaBench; no further search this round.
- Papers and pages: the Kaggle page and codebook; MulTaBench (Arazi et al. 2026, https://arxiv.org/abs/2605.10616), App. B.2: "Restaurant listings from the Zomato platform covering Bangalore, India. The target is the aggregate user rating."
- Metric: none found (a Kaggle dataset, not a competition; MulTaBench's R² is benchmark-wide, MET-5), so the fallback `rmse`; inputs none.
- Risks for /add-dataset: `reviews_list` holds the reviews with their own star ratings and `votes` counts the ratings, so both are built from what the target averages (LEAK-10), and `dish_liked` comes from the reviews too (the raw 574 MB file was not opened); `rate` is a string with "NEW" and "-" entries; repeated restaurants across listings (LEAK-16, grouped split); `phone`, `url` and `address` identify a restaurant; one snapshot without opening dates, so no temporal split.
- Priority: gap 0 (business & marketing, regression not thin), use case 0 (the page names the actor, the fit is approximate), source + (a documented scrape with a codebook), shape + (41,665 rows; categorical, text and numeric), risk - (review columns built from the ratings; repeated rows).

**Assessment (AI, 2026-11-01):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616) as "Zomato Restaurants"; split out on 2026-11-01 from the note on `zomato`, which links a different Kaggle dataset.
- as published: 41,665 rows; 8 structured, 7 text, 0 image features (MulTaBench Table 3); target: Aggregate user rating.
- Why: Predict a Bangalore restaurant's aggregate Zomato rating
- Notes: Text-tabular; raw user review text and vote count are features (posted alongside the rating). The record zomato is tagged CARTE/TexTabBench but links a different Kaggle dataset (anas123siddiqui/zomato-database, partly generated); MulTaBench's source is the Bangalore scrape, so the record's link may be wrong.
