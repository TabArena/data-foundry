---
unique_name: craigslist_used_vehicles_f150
name: Craigslist used vehicles, Ford F-150 asking prices across repeated scrapes
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Entities: Recur'
- Dated Event Log
original_source: Kaggle
year: '2018'
collection_period: Oct 2019 - May 2021; Oct 2026
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data
- https://github.com/AustinReese/UsedVehicleSearch
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 2: the only public table found with asking prices of one car model over repeated, dated scrapes: Ford F-150 listings from Austin Reese's Craigslist scrapes on Kaggle, 6,600 to 13,400 trucks per scrape, October 2019 to May 2021 plus one scrape of 2026, 78,955 over 2019-2021 (measured 2026-11-05 and 2026-11-25); a model trained on earlier scrapes errs 15% to 25% more on the next one than a random split within it shows. Deep pass; the first screening of this record.
- Source: Kaggle `austinreese/craigslist-carstrucks-data`, Austin Reese (uploader), CC0; the card: "I built a scraper for a school project and expanded upon it later to create this dataset which includes every used vehicle entry within the United States on Craigslist", "For previous listings, check older versions of the dataset"; scraper code on GitHub (AustinReese/UsedVehicleSearch, created 2018-09-21, GPL-3.0). First publication: "Initial release", Kaggle version 1 of 2018-10-10 (title then "Craigslist Cars+Trucks Data"; Wayback capture of 2019-07-08 lists versions 1-6 of 2018-10-10, 2018-11-01, 2018-11-16, 2018-11-20, 2018-11-22, 2019-06-09). Those versions are gone: the current history (Kaggle CLI, 2026-11-25) starts at version 1 of 2019-10-08 and runs to version 11 of 2026-11-05 (now titled "Used Cars Dataset"). `year` 2018 (PROV-9: a Kaggle upload that grew over its versions takes its first version's year), set; `original_source` Kaggle (PROV-8: the data first appeared there). No paper by the uploader; none found that defines a task on it. As published: one CSV per version, one row per listing, about 26 columns (price, year, manufacturer, model, condition, cylinders, fuel, odometer, title_status, transmission, VIN, drive, size, type, paint_color, region, lat/long, state, the posting text, image and listing URLs; `posting_date` only in versions 8, 10 and 11; version 2 has the model in `make` and the place in `city`). Read on 2026-11-05: versions 2 and 4 to 11, uploaded 2019-10-14, 2020-01-07, 2020-03-22, 2020-06-17, 2020-09-16, 2020-12-03, 2021-04-20, 2021-05-06 and 2026-11-05.
- Scope of the filter: this record is the Craigslist upload with one model kept (manufacturer `ford`, model matching `^f-?150`), a row selection of the definition, not another source. No other record holds this upload (searched craigslist, austinreese, UsedVehicleSearch), so it is in scope as the upload's one record (PROV-4); a later all-makes or other-model record of the same upload would be a cut of it (PROV-6) unless it gives a distinct task, and should be decided here, not as a new record. The one-model selection is the use case's population (pricing an F-150 against F-150s), not a `Selection Bias`. Recommend: `name` lists the published names ("Used Cars Dataset / Craigslist Cars+Trucks Data", records.md), and the F-150 filter is stated in the definition and in this comment; `unique_name` stays (renaming breaks links; the curator's call while the record is new). The F-150 was picked on 2026-11-05 as the most-listed model (Honda Civic 4,400 to 6,100 listings per scrape is the runner-up).
- Use case: a seller (owner or dealer) setting an asking price for a used F-150, or a buyer or marketplace judging one, from the advert's fields, after the data was collected, so later markets; fit approximate: the target is the asking price, not a sale price, and the use case is the curation's (the card names none). Collection: `Samples: Over Time`, `Time: Dated` (each row comes from a dated scrape, the version's upload date; versions 8, 10 and 11 also carry `posting_date`, each spanning about the month before its scrape), no target tag (the price exists with the advert), `Entities: Recur` (6.6% of rows carry a VIN seen in an earlier scrape; only 47.5% of rows carry a VIN); `collection_period` Oct 2019 - May 2021; Oct 2026 (the versions read; the 2018-2019 scrapes are no longer downloadable). Type `Dated Event Log`: each row is one listing with its scrape's date; most trucks appear once, so not panel data (SPLIT-34).
- Split: leaf L-ORDER.windows (Temporal · windows on the time key) because the model meets listings after the data (LOG.meets), every row has its scrape (ORDER.order), eight scrapes give seven windows (versions 9 and 10, two weeks apart and sharing 27% of listing ids, merged into one), of which the last three tested with 83% to 88% of rows before them in training (ORDER.windows), and the table is large (ORDER.small no); no gap (the price arrives with the advert). Open: whether the 2026 scrape (a five-year gap, about 5,700 trucks) is a further window; whether a truck relisted across the cutoff stays (a dealer knows its earlier price, SPLIT-13) or is dropped; the window list (first windows from Sep 2020 meet the 50% floor).
- Siblings and duplicates: `fiat_500` (`Yes`, shipped; one crawl of automobile.it, 1 April 2020; its Review issue 7 recommends keeping it until this record replaces it, B); `us_used_cars_cargurus` (`TBD -> Yes`, one CarGurus crawl of September 2020, all makes, not downloaded), `dvm_car_uk_used_car_adverts` (`TBD -> Yes`; later adverts are 2019 registrations only), `autoscout24_car_listings_2025`, `used_cars_pakistan`, `used_cars_saudi_arabia`, `pakwheels_used_cars_2022`, `used_cars_24`, `used_cars_benz_italy`, `used_cars_dataset_cardekho` (each one crawl, all makes, other markets; none a duplicate, PROV-4). External: Zenodo 10457828 is someone else's CC BY 4.0 copy of one version; no benchmark collection found that carries it.
- Better data: found as better data for `fiat_500`. Nothing better found for this one: the fiat_500 checks of 2026-11-05 and 2026-11-25 (counted on the files) found the Illinois dealer listings (F-150 17,798, daily June 2018 to May 2020, but mileage 0 in 49% of used-car rows), European sold listings (one three-week crawl of 2026), DVM-CAR, otomoto.pl, eBay-Kleinanzeigen, the European 2M and Malaysian snapshots (one crawl, a few weeks, or all makes without dates); a Kaggle search of 2026-11-25 found no other dated multi-scrape table of one model.
- Papers and pages: the Kaggle card and the GitHub scraper; student projects and notebooks use the all-makes table for price regression (e.g. github.com/rajtulluri/Predicting-Used-Car-prices-Craigslist, github.com/kiranrangaraj/Machine-Learning-Used-Car-Price-Predictor); no peer-reviewed paper found.
- Metric: none from the source (a Kaggle dataset without a task or leaderboard; looked at the card, the GitHub README and a web search), so the regression fallback `rmse` (MET-1) on the price in dollars, with the target shippable as log (MET-3); inputs none.
- Baselines measured 2026-11-25 (untuned LightGBM, 400 trees, learning rate 0.05, 63 leaves, and a ridge regression, both on the log price; RMSE in dollars; placeholders and relisted VINs dropped):

  | Test scrape | Test trucks | GBM, earlier scrapes → this one | GBM, random within this scrape | Gap | Ridge, earlier → this one |
  |---|---|---|---|---|---|
  | Sep 2020 | 6,449 | 5,944 | 4,794 | +24% | 7,143 |
  | Dec 2020 | 8,472 | 5,110 | 4,428 | +15% | 6,823 |
  | Apr-May 2021 | 12,952 | 6,308 | 5,043 | +25% | 7,109 |

  LightGBM beats the ridge by 10% to 25% in every window. The median asking price of comparable trucks (2013-2015, 60,000 to 120,000 miles) moves from 22,999 (Oct 2019) to 20,900 (Jun 2020) to 26,700 (May 2021).
- Risks for /add-dataset: (1) fields typed in by the poster: the trim only inside the model string (600 to 900 spellings per scrape; the first word after "f-150" was used), condition, cylinders, odometer (over 500,000 set missing), title status (CLEAN rules); (2) the posting text holds phone numbers (73% of the F-150 texts of May 2021): drop it with url, id, VIN and image fields (P1, never shipped); (3) relisted trucks across the split: 5,236 rows (6.6%) carry a VIN of an earlier scrape and are priced better than fresh ones (Sep 2020 RMSE 4,190 against 6,241; Apr-May 2021 4,934 against 6,551), while trucks without a VIN cannot be linked, so a relisting is a near-copy only partly detectable (SPLIT-13, LEAK-42); dropping them leaves the gap at 15% to 25%; (4) placeholder prices: the price filter 1,000 to 150,000 removes the 0 and 1 placeholders (5% to 10% of raw F-150 rows); 341 rows (0.4%) left with a sequence or repeated-digit price (12345, 99999) or under 5,000 for a 2015-or-newer truck (a down payment), to drop (minimal preprocessing: they differ for non-target reasons); (5) schema drift across versions (v2's `make`/`city`; `posting_date` in three versions) and within-scrape repeats (one row per VIN, then repeats of year, odometer, price and region dropped); (6) asking price, not sale price (USE-5). Versions 1 (2019-10-08, 177 MB) and 3 (2019-12-02) of the current history were not read. Licence: CC0 on Kaggle; Craigslist's terms forbid scraping (a note, EV-4).
- Priority: gap 0 (business & marketing, regression and temporal are not thin), use case 0 (ours: the card names no decision; fit approximate), source + (a versioned upload with a data card and its scraper published), shape + (6,600 to 13,400 trucks per scrape, mixed types, seven dated windows), risk - (relisted trucks across the split, a near-copy leak only partly linkable).

CC (2026-11-25, Andrej): created as the replacement candidate for fiat_500 (Review issue 7, the better-data check of 2026-11-25), to be screened; one model (Ford F-150) of the Craigslist used-vehicle scrapes, windows by scrape.
