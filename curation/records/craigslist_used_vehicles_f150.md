---
unique_name: craigslist_used_vehicles_f150
name: Craigslist used vehicles, Ford F-150 asking prices across repeated scrapes
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Entities: Recur'
- Dated Event Log
original_source: Kaggle
year: '2018'
collection_period: 2018 - May 2021; Oct 2026
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data
- https://github.com/AustinReese/UsedVehicleSearch
v2_path: datasets/_dev/tabarena-v0pt2/craigslist_used_vehicles_f150/dataset.py
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

**Assessment (AI, 2026-11-25):** collection facts corrected from the data (/add-dataset): `collection_period` 2018 - May 2021; Oct 2026 (was Oct 2019 - May 2021; Oct 2026). Kaggle version 1 (uploaded 2019-10-08, 699,316 rows) is an older scrape, not the start of the 2019 series: Craigslist listing ids follow the posting date (correlation 0.99998 on versions 8, 10 and 11), and all of version 1's ids lie about 277 million ids, over a year of postings, before version 2's; it shares no listing id with version 2 and also holds Canadian sites. Version 3 (2019-12-02) is a separate scrape too (1 to 5 listing ids shared with versions 2 and 4). The definition reads versions 1 to 10 as nine scrape periods (9 and 10 merged), 108,303 F-150 rows.

**Assessment (AI, 2026-11-25):** screening facts corrected further from the data and the review panel (/add-dataset): the upload holds nine scrape periods, not eight: version 3 (2019-12-02) is a scrape of its own and version 1 an older 2018 scrape that also holds Canadian and Mexican sites (437 and 46 F-150 rows, dropped), both read; so the split has five test windows, Mar 2020 to May 2021, training on 52.3% to 88.6% of the rows, not three from Sep 2020 at 83% to 88% (the Mar 2020 window clears the 50% floor only with version 1, whose order is measured from listing ids and whose date is inferred). Relisted trucks are 8.2% of the rows on the shipped frame (46.5% carry a VIN), not 6.6% (47.5%). The windows are named by upload: their postings end 5 to 10 weeks before it in versions 2 to 6, so the Mar 2020 window is a pre-COVID market.

**Assessment (AI, 2026-11-25):** review panel (full): ship after changes; disputed: USE-6 against P1 (the advert's title as an input), LEAK-42 (the drop of one truck's copies across sites, a key rebuilt from the features; relistings across scrapes kept under verdict 3), SPLIT-14 (Mar 2020 clears the floor only with version 1); for the curator: issues 1-2 and the horizon H. Priority 3: gap 0, use case 0, source +, shape +, risk 0 (gap: no thin domain, problem type or regime; use case: ours, the card names none; risk: the one leak, relistings, is kept on purpose and moves the RMSE by under 2%, and no open issue threatens validity).

## Review

**Outcome:** added. Ford F-150 asking prices from nine nationwide Craigslist scrapes on Kaggle (2018 to May 2021, 105,134 trucks), split into five later-scrape windows; the AI recommends shipping it. Validity: every input is in the advert when it is written; the one leak, a truck relisted in a later scrape, is kept on purpose as a repost a dealer knows (no listing id appears in two periods; dropping the linked ones moves the RMSE by -1.6% to +1.9%). Value: untuned LightGBM beats a linear model in every window (RMSLE 0.312 against 0.404, dummy 0.859; RMSE in dollars 4,839 against 6,052); model year carries most of the signal (R² 0.666 without it). The panel's changes are applied: one row per truck also across Craigslist sites (issue 2), RMSLE from context as for every other asking-price task, charm prices such as 9,999 kept, impossible and placeholder values set missing, the seller type (owner or dealer) shipped, and the notes corrected. `dataset check`: 0 errors, 0 warnings, 1 info; the four warnings of the build-up are accepted with reasons. Not built.

**Main points:** Ship the advert's title, carried in the url, as an input (issue 1)? Confirm the drop of one truck's copies across Craigslist sites (issue 2), and sign off the five one-scrape windows (H), whose oldest clears the 50% floor only with the inferred-date 2018 scrape in training.

**Horizon:**

* **Verdict:** keep the five one-scrape windows, Mar 2020 to May 2021 (A); confident on the order, and the window length is our assumption.
* **Length:** one scrape, about five weeks of postings (seven for the merged May 2021 scrape); the source says only that the data was scraped "every few months", so that the refit step equals the scrape is ours. Uploads are 5 to 21 weeks apart.
* **Gap:** none for the label: the price arrives with the advert. The scrape schedule leaves postings unseen before each window, by listing id about 7, 3, 16, 7.5 and 15 weeks before the Mar 2020, Jun 2020, Sep 2020, Dec 2020 and May 2021 windows; a pricing guide refit daily has no such gap, so the windows test a longer horizon than in practice.
* **Time frame:** the windows are named by upload, the source's only date for most versions. By listing id their postings run about Jan to mid-Feb 2020 (before COVID-19), Mar to Apr 2020 (the pandemic's start), Aug to early Sep 2020, 28 Oct to 3 Dec 2020 (measured from `posting_date`) and mid-Mar to 5 May 2021, across the 2020-21 rise in used-truck prices. The Mar 2020 window trains on 52.3% only because version 1, an older scrape, is in training: without it 43.5%, under the floor[^h14]. Version 1's order is measured (listing ids follow posting dates, r = 0.99998, and all its ids lie over a year of postings before version 2's); only its calendar date, 2018-10-10, is inferred. The 2026 scrape is left out: five years after the others, with model years training never shows.

  | Window | Postings (by listing id) | Test trucks | Training share | Training share without version 1 |
  |---|---|---|---|---|
  | Mar 2020 | Jan to mid-Feb 2020 | 13,087 | 52.3% | 43.5% |
  | Jun 2020 | Mar to Apr 2020 | 10,015 | 64.8% | 58.3% |
  | Sep 2020 | Aug to early Sep 2020 | 6,405 | 74.3% | 69.5% |
  | Dec 2020 | 28 Oct to 3 Dec 2020 | 8,631 | 80.4% | 76.8% |
  | May 2021 | mid-Mar to 5 May 2021 | 12,008 | 88.6% | 86.5% |

* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | One scrape per window (implemented) | Five windows, each one scrape, trained on every earlier scrape, no gap | 5: 13,087, 10,015, 6,405, 8,631 and 12,008 trucks | every scrape whose training side keeps half the rows; the newest scrape tested; a pre-COVID, a COVID-start and three later markets | five against the nine the table's size asks for; the oldest window clears the floor only with the inferred-date 2018 scrape |
  | B | A plus Jan 2020 | Adds the Jan 2020 scrape as a sixth window, your exception under the floor | 6: A's five and 12,616 trucks | one more test period | trains on 40.3%; adds a second pre-COVID winter the Mar 2020 window already covers |
  | C | Versions 9 and 10 as two windows | Splits the merged May 2021 period | ruled out | none found | the two overlap in posting time and share 26% of their listings, so they are no one-unit windows |
  | D | Cuts inside each scrape by listing id | Finer windows within a scrape | ruled out | more windows | a scrape's early postings are the ones still unsold at the scrape, so the cut mixes in that selection |

* **Recommendation:** A, as the split auditor recommends: it is every eligible scrape, and B adds only a second pre-COVID winter at your exception. **Decision:** A or B?

  [^h14]: **SPLIT-14** (Must): every window trains on at least 50% of the data; a window under 50% is the curator's exception, down to 30%. **SPLIT-12** (Should): the horizon is a human judgment from the source, which the curator signs off with the test windows of every new temporal dataset.

**Issues for the curator:**

1. **Ship the advert's title, which the url carries, as an input?**

   * **Problem:**
     - The url carries the advert's title as a slug in 99.9% of rows, and it names the trim and cab that the model string hides in the 59% of rows that read a bare "f-150".
     - Trim and cab flags parsed from the slug, with the seller type, cut the RMSE by 6.8% to 10.4% in every window, and the largest May 2021 errors are premium trims listed as a bare "f-150".
     - The definition never reads the title, for privacy, but a scan of all 108,303 slugs found no phone number, and its name hits were all place names; 214 hold the asking price as a number.
   * **Background:** the title is what a poster writes first and what a buyer reads first ("2012 ford f150 v8 5.0l 4x4"); an input known at the prediction point is a legitimate one, and dropping it changes the task[^u6]. The definition drops the url as an identifier; the seller type it also carries now ships (owner or dealer, the poster's Craigslist section), and the title would be a second meaning taken from it[^c3]. The same reasoning would reach the VIN's series and engine characters (about 60% of the raw rows carry a VIN), which the panel did not propose to ship.
   * **Experiments:** untuned LightGBM, RMSE in dollars, on the frame before the panel's changes (the domain practitioner, measured); about 27 trim and cab flags parsed from the slug with a fixed list, plus the seller type, so the gain is option C's.

     | Window | RMSE without them | With slug flags and seller type | Seller type alone (range over the windows) |
     |---|---|---|---|
     | Mar 2020 | 3,905 | 3,521 (-9.8%) | -0.2% to -0.7% |
     | Jun 2020 | 4,084 | 3,660 (-10.4%) | |
     | Sep 2020 | 5,936 | 5,488 (-7.5%) | |
     | Dec 2020 | 5,121 | 4,601 (-10.2%) | |
     | May 2021 | 6,307 | 5,880 (-6.8%) | |

     The privacy scan (the mediator, measured on 108,303 slugs):

     | Pattern | Slugs |
     |---|---|
     | phone number or 7 or more digits in a row | 0 |
     | "www" | 1 ("lowwww") |
     | person-name hits | 0 (all were place names: san-jose, santa-maria) |
     | "call" or "text" | 315, none with a number |
     | the asking price as a number | 214 (0.2%; some only a model year equal to the price) |

   * **Consistency:** mercari_price_suggestion ships the item's name as text; a fixed list of trims of our own is a feature the feature-building rule does not cover[^c19], which is why the builder kept the model string as text and the precedent check calls a trim list "a feature of our own invention".
   * **Unknown:** the gain of the slug shipped as text (option B); only the flags were measured.
   * **Panel:** the critic asks for slug-derived trim and cab flags by default; the advocate would ship the slug after the privacy scan, which is now done; the mediator leans to the slug as text.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave the title out (implemented) | No title input; a note says why | nothing of the posting text ships; the task stands without it | the task prices an advert without its headline; premium trims listed as a bare "f-150" stay the largest errors |
     | B | The slug as text | Ships the slug as a second `string` feature, with the city prefix and any number of 1,000 or more that is no model year removed | the source's own text, no list of ours; it holds the trim words behind the measured gain | a text field of the poster's, checked for names and numbers but free text all the same; its own gain not measured |
     | C | Trim and cab flags from the slug | Ships about 27 flags parsed from the slug with a fixed list | no free text ships; the gain as measured (6.8% to 10.4% with the seller type) | a list of our own invention that the feature-building rule does not cover |

   * **Recommendation:** B, the mediator's lean: it is the source's own text with the price copies removed, the scan found no personal data, and it adds no list of ours. **Decision:** A, B or C?

   **Notes for the AI:** on B, in `_clean` take the slug from the url (`/d/<slug>/<id>.html`; check the url form of versions 1 to 3 first), drop the city prefix before the model year, turn hyphens into spaces, and remove every number of 1,000 or more that is not a model year between 1975 and the scrape year + 1; add it to `string` in `_feature_types` and say so in the notes (the title stays dropped from the posting text, which is never read). On C, parse the trim and cab words (raptor, platinum, king ranch, lariat, limited, harley, xlt, xl, stx, fx4, tremor, supercrew, supercab, regular cab, 4x4) from the slug and the model string into flags and record the list. Either way re-run `dataset check`, the leak probes and the task probe, and re-scan the shipped text for digits of 7 or more and for names.

   [^u6]: **USE-6** (Must): anything known at the prediction point is a legitimate input; dropping it changes the task. **P1** (ethics) ranks above it: the posting text holds phone numbers in 70-80% of the F-150 adverts and is never read.
   [^c3]: **CLEAN-3** (Should): keep an identifier that carries meaning and process it into that meaning.
   [^c19]: **CLEAN-19** (Should): we build a feature only when it removes a leak, restores meaning the source destroyed, or is what a data scientist on this task would build because the raw data cannot be used as it is.

2. **Confirm the drop of one truck's copies across Craigslist sites within a scrape?**

   * **Problem:**
     - A dealer's truck posted on several Craigslist sites in one scrape stayed once per site; the definition now keeps one row per model year, mileage and price within a scrape where the mileage is no multiple of 1,000.
     - Among such groups that carry VINs, 99.8% of 11,280 hold one VIN, but the link is rebuilt from the features, so the drop is your call[^l42].
     - The drop is 3,481 rows (3.2%), 9.5% of the May 2021 window, and the price's distribution does not move.
   * **Effect on the task:** the copies never cross the split, since a scrape is never cut, so they are no leak; they scored one truck several times in a test window (one truck at 83,066 miles stood 39 times in May 2021) and weighted dealers who post widely in training.
   * **Experiments:** measured on the definition before and after the step.

     | Scrape | Rows dropped |
     |---|---|
     | Oct 2018 | 1.5% |
     | Oct 2019, Dec 2019, Jan 2020 | 2.0% to 2.3% |
     | Mar 2020 | 2.5% |
     | Jun 2020 | 2.7% |
     | Sep 2020 | 2.9% |
     | Dec 2020 | 3.5% |
     | May 2021 | 9.5% |

     | Price (dollars) | 10th percentile | Median | 90th percentile |
     |---|---|---|---|
     | before the drop | 3,500 | 14,995 | 33,995 |
     | after the drop | 3,500 | 14,950 | 33,919 |

     Untuned LightGBM, RMSE in dollars, with the copies dropped from both sides (the column auditor, before the panel's other changes; its drop took every mileage over 1,000, wider than A):

     | Window | As before | Copies dropped |
     |---|---|---|
     | Sep 2020 | 6,442 | 6,427 |
     | Dec 2020 | 4,726 | 4,734 |
     | May 2021 | 5,655 | 5,744 (+1.6%) |

     Round mileages match by VIN too (98.5% of 741 groups); dropping those as well would take 2,713 rows more.
   * **Consistency:** fiat_500 keeps one row per car whatever the place. Relistings across scrapes are a different case and stay: no listing id appears in two periods, so each is a new advert, at a new price in 61.6% of cases, a repost a dealer knows[^l42t].
   * **Panel:** the critic and the advocate both ask for the drop; the mediator recommends the milder step on odd mileages.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Odd mileages (implemented) | One row per model year, mileage and price within a scrape where the mileage is no multiple of 1,000 | one truck, one row, as fiat_500; an odd mileage on two sites at one price is near-certainly one truck | the site kept is arbitrary (the last); round-mileage copies stay |
     | B | Every mileage | As A, also for round mileages | removes the remaining copies (98.5% VIN agreement) | 2,713 rows more on a weaker link: two trucks at 120,000 miles and one price are plausible |
     | C | No cross-site drop | One row per truck and site, as before, with the note corrected | no rows lost | one truck scored several times in a test window, 9.5% of May 2021 |

   * **Recommendation:** A: the link is near-certain on odd mileages, the target's distribution does not move, and the rule asks for one row per unit. **Decision:** A, B or C?

   **Notes for the AI:** A is the `odd_mileage` step after the per-site dedup in `_clean`. On B, drop the `odd_mileage` mask (keep the step for every row with a mileage) and update the counts in the notes; on C, remove the step and say "one row per truck and site" in the notes and in `task_summary`. Re-run `dataset check` and the task probe.

   [^l42]: **LEAK-42** (Must), verdict 2: copies of one record (entered twice, listed again) go down to one row per unit; a key rebuilt from the features, and every drop, is a discussion point for the curator, with the share dropped and the target's distribution before and after.
   [^l42t]: **LEAK-42** (Must), verdict 3: a temporal split fits when the use case sees the unit again at prediction time (a renewal, a repost the moderator has seen). **SPLIT-13** (Should): an entity that recurs across the cutoff is part of the task when the model predicts for known entities.

**Review panel:** ship after changes (mediator). Claims: 22, 15 hold, 6 refuted (all fixed), 1 untested (version 1's calendar date). Blind review: would benchmark with changes; its main concern, one listing in several scrapes, is refuted (no listing id appears in two periods). Task gamer: a relisted truck's earlier price gains 0.9%, near noise. Agreed: the split, the relistings kept, RMSLE, the cleaning fixes, the seller type. Disputed: the advert's title as an input (issue 1); the horizon (H). Agreed by both sides but left to the curator: the cross-site drop, a key rebuilt from the features (issue 2).

<details><summary>Mediator</summary>

I recommend shipping after changes. The advocate and the critic agree on almost everything. My two checks settled the main fact under dispute. Two calls are left for the curator; neither puts validity at risk.

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL holds (CC0; posting text, title, VIN and id are never shipped). USE-1 and USE-5 hold (fit approximate:
  asking price, fields typed by the poster). USE-8: fit_reason must name the relistings as a leak kept on purpose, not
  a gap in the fit. SPLIT-36: leaf L-ORDER.windows confirmed on its own. SPLIT-14 holds (51.6 to 87.8% in training;
  the Mar 2020 window clears the 50% floor only because version 1 is in training). LEAK-42 verdict 3: relistings across
  scrapes kept with a note (0 listing ids appear in two periods; the gain is about 1%). LEAK-42 verdict 2 triggered
  within a scrape: copies of one truck on several sites, fixed (change 1).
Value: TP holds (LightGBM R² 0.867 against a linear model's 0.777, paired SE 0.004). MET-11 departure fixed: rmsle from
  context (change 2).
Quality: CLEAN-11 (the $9,999 price regex, values impossible for an F-150) and CLEAN-10 (placeholder mileages) fixed.
  CLEAN-3: the seller type (owner or dealer) is recovered from the url. Several notes are corrected (EV-1).
Weighed: size +, source + (versioned scrapes, scraper published), drift + (an honest later market), the only dated
  multi-scrape data of one model + (replaces fiat_500), use case 0 (ours; the source names none).
For the curator: issue 1, whether the advert title goes in as an input (a weighing call); issue 2, confirm the
  cross-site drop (a key rebuilt from the features); issue 3, sign off the horizon.
```

**Changes to make now (no decision needed)**

1. **One row per truck within a scrape** (LEAK-42 verdict 2, Must; precedent fiat_500). For rows whose mileage is not a multiple of 1,000, take `region` out of the second dedup key at `dataset.py` as reviewed (line 216).
   - **Decisive experiment**: before the VIN dedup, I took rows that share a scrape, model year, odd mileage and price on two or more sites. Among those carrying VINs, 99.8% of the 11,280 groups have one VIN. So the link is real: they are the same truck.
   - **What it removes:** 3,475 rows (3.2%): 1.5 to 3.5% of each scrape and 9.5% of the May 2021 window. The price distribution does not move (median $14,995 → $14,985; 10th and 90th percentiles $3,500 → $3,500 and $33,995 → $33,950).
   - Round mileages also match by VIN (98.5% of 741 groups), so drop `region` from the key for every row with a mileage if the curator prefers. The odd-mileage-only version is the milder step.
2. **Metric:** `Metric.from_context("rmsle", target_transform="log")`, with the reason worded as for immoscout (MET-11 Must, its own example; MET-3; precedent F1). Both sides agree, and no fact sets this dataset apart.
3. **Placeholder prices** (CLEAN-11): drop `9999` from `PLACEHOLDER_PRICE` and match only 5 or more repeated digits, plus 1234, 12345 and 123456. This restores 443 charm prices at $9,999 and the rows at $8,888, $7,777 and $6,666.
4. **Impossible values become missing, rows kept** (CLEAN-11), one rule each, with its count in the notes:
   - `drive == "fwd"` (2,465 rows);
   - cylinders other than 6 or 8 (219);
   - `size` compact or sub-compact (191);
   - `fuel == "electric"` before 2022 (11);
   - coordinates outside the US (about 53).
5. **Placeholder mileage** (CLEAN-10): an odometer under 100 on a truck at least 2 model years old becomes missing (547 rows).
6. **Seller type** (CLEAN-3, USE-6): ship `seller` (owner or dealer, from `/cto/` and `/ctd/` in the url) as a categorical. It carries no personal data. Both sides agree.
7. **Target copied into the model string** (LEAK, weak): strip `\$[\d,.]+` from `model`. It affects 12 rows, 3 of which hold the exact price. Cheap and safe.
8. **Wording** (EV-1, USE-8):
   - Scrapes are dated by upload. Remove "Mar 2020 … start of COVID-19": that window holds Jan to mid-Feb 2020 postings, and the pandemic's start falls in the Jun 2020 window.
   - State the 3 to 16 unseen weeks before each window.
   - Correct the Canadian rows to 437 (not 483).
   - `fit_reason`: name the relistings as a leak kept on purpose, with the share whose price is unchanged per window (4.4 / 8.2 / 0.9 / 2.0 / 1.3%).
   - Anomaly line: the drop in missing mileage is Craigslist's form change around 30 Nov 2020.
   - Builder issue 2: without version 1, the Mar 2020 window trains on 42.9%, below the floor.
   - Recompute the row counts and training shares after changes 1 to 5. The Mar 2020 window stays above 50% by my estimate (about 52%).
   - Tag version 1's period `Time: Inferred`, as for diabetes_130_us.
9. **Proposed warnings:** accept all four. `dataset_conflicting_duplicate_rows` gets this reason: 93.6% of 1,708 same-year, same-mileage, different-price groups share a VIN, so they are one truck at two prices within one scrape. A scrape is never cut by the split, so they stay together as LEAK-42 verdict 2 asks.

**Issues for the curator, ranked**

**1. Ship the advert title (the url slug) as an input? (USE-6 Must against P1, CLEAN-19; a weighing call)**
- **Problem:** the title is in every advert and in 99.9% of urls. It holds the trim and cab that a bare "f-150" model string hides, and the largest May 2021 errors are premium trims listed as a bare "f-150".
- **Effect:** the slug plus the seller type cut RMSE by 6.8 to 10.4% in every window (domain practitioner). The seller type alone gives 0.2 to 0.7%.
- **The P1 check is now measured** (108,303 slugs):
  - 0 phone numbers and 0 runs of 7 or more digits;
  - 1 slug with "www" in it ("lowwww");
  - the name hits were place names (san-jose, santa-maria);
  - 315 contain "call" or "text", without a number.
  - New fact: 214 slugs (0.2%) hold the asking price as a number, and some of those matches are only a model year equal to the price.
- **Critic's best case:** USE-6, dropping an input changes the task; ship slug-derived trim and cab flags by default.
- **Advocate's best case:** USE-6 makes the title a legitimate input but does not require it; the title was never read on purpose.
- **Against the flags:** builder issue 6 and precedent checker call a fixed trim list "a feature of our own invention" that CLEAN-19 does not cover.
- **Options:**
  - (a) ship the slug as a `string` feature, with the city prefix and any number at or above 1,000 that is not a model year removed;
  - (b) slug-derived flags;
  - (c) leave the title out, with a note.
- **Decision needed:** a/b/c. I lean to (a): it is the source's own text with the price copies removed, and it adds no list of our own.
- **Same question:** decoding the VIN's series and engine characters (CLEAN-3; about 60% of rows carry a VIN).

**2. Confirm the cross-site drop (LEAK-42, last paragraph: a key rebuilt from the features, and every drop is a point to discuss).** Both sides agree and the VIN test confirms the link. The drop is 3.2% of rows (9.5% of May 2021) and the target's distribution does not move. Decide: odd mileages only (recommended) or every row with a mileage.

**3. Sign off the horizon (SPLIT-14/15).**
- Option A, as implemented: 5 windows of one scrape each.
- Option B adds Jan 2020, which trains on 39.8% and would be your exception.
- C (versions 9 and 10 as separate windows) and D (cuts by listing id inside a scrape) are ruled out on the measurements.
- The split auditor recommends A. B adds only a second pre-COVID winter.

**Agreed facts**

- 108,303 trucks in 9 periods. Listing ids follow posting dates (r = 0.99998). No posting time overlaps between scrapes, except versions 9 and 10, which are merged. 0 listing ids appear in two periods.
- Every feature is known when the advert is written. The only leak is relisted trucks: 8.0% of rows, 2 to 17% of a window. Dropping them moves RMSE by −1.6 to +1.9%.
- Baselines: dummy RMSE 14,725, linear 5,983, LightGBM 4,842. Model year carries 82% of the split gain; without it R² is 0.632. Prices drift from about $14.5k (2019 to Jun 2020) to $18.5k–19.5k (Sep 2020 on).
- The dearest 10% of trucks carry 36 to 52% of the squared dollar error.
- Version 1's order is measured; its date is inferred.
- No better dated, multi-scrape data of one model exists (fiat_500 check).

**Task-gamer exploits**

| # | Exploit | Rule | New or known | Measured against the note |
|---|---|---|---|---|
| 1 | Earlier price of the same truck from an earlier scrape | LEAK-42 verdict 3, SPLIT-13 | Known: the "Potential leak, kept on purpose" note | +$42 mean (0.9%), +$129 in Jun 2020. The note gives no number; builder issue 3's −1.6 to +1.9% fits. The gamer's worry that a copy is a listing still live before the cutoff is refuted (0 ids in two periods). Not an issue; add the gain to the note (change 8). |
| 2 | Counts over the whole table (copies within a scrape, copies across dates, per coordinate) | LEAK-30 (statistics over all rows), done by the participant | New | +$14, at noise ($8 to $47). No fix needed; change 1 also removes most of the copies within a scrape. |
| — | Stale 2018 scrape; fitting on log vs dollars | P4 over P6 (forest_fires tension); MET-3 | Not an exploit | A modelling choice for participants. The log-vs-dollar point goes away under RMSLE. |

**Consistency with precedent**

- **Metric:** now follows diamonds, immoscout, perth, house_sales and mercari (F1).
- **Dedup:** now follows fiat_500's one row per car (F2). The fact that copies never cross the temporal split does not set the case apart, because one truck is still scored several times in a test window.
- **Relistings kept:** follows house_sales, melbourne_housing_market, liberty_mutual and diabetes_130_us. Add a Cases row to LEAK-42 / SPLIT-13: a relisting is a new advert, at a new price in 61.5% of cases.
- **Version 1:** follows diabetes_130_us (F3; `Time: Inferred`).
- **2026 scrape left out:** departs from g_research with stated reasons (a five-year gap and columns of its own), so it stands.
- No departure is left without a fact that sets it apart.

</details>

<details><summary>Claim audit</summary>

I tested 22 claims for `craigslist_used_vehicles_f150`. 15 hold, 6 are refuted and 1 is untested. None of the refutations threatens the task: the split, the target and the absence of a leak all hold. The six problems are a metric that breaks precedent, three cleaning steps that do something other than what the notes say, and two wording or number fixes.


**Claims**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Metric: fallback RMSE in dollars, target shipped as log; "the task makes none obvious" | `metric`, README Metric block | Checked MET-11's "context" origin and similar price datasets; split the squared error by price | **Refuted** (as a choice) | MET-11's own example of a "context" metric is "a price's error matters relative to the price, so `rmsle`". Every price dataset here with no source metric uses `Metric.from_context("rmsle")`: diamonds, immoscout_german_house_prices (also an asking price), and the house-price sets. With untuned LightGBM, the dearest 10% of trucks carry 36–52% of the squared dollar error in every window. LightGBM ranks above ridge on both RMSE and RMSLE | MET-11, MET-3, precedent |
| 2 | The metric is computable on every fold | `metric` | Scored a median dummy and a perfect prediction with the declared scorer on each fold | Holds | Dummy RMSE 16,126 / 15,123 / 15,969 / 10,662 / 10,923; perfect prediction 0. No scoring columns needed | MET-2 |
| 3 | Placeholder prices are "a repeated digit such as 99999, a sequence such as 12345" | `curation_comments`, `PLACEHOLDER_PRICE` | Counted what the regex removes; compared $9,999 trucks with trucks at nearby prices | **Refuted** | The regex removes 530 rows, 443 of them at **$9,999**. That is a charm price, not a placeholder: median model year 2008 and 147,973 miles, the same as $9,995 (2009, 160,919) and $10,000 (2007, 140,300). Its count fits the pattern of the neighbouring thousands (8,999: 357; 9,999: 443; 10,999: 361). Also removed: 8888 (19), 7777 (10), 6666 (2). This drops rows by the target's own value | CLEAN (minimal preprocessing), selection on the target |
| 4 | "One row per truck within a scrape period … dealers post one truck in several sites" | `curation_comments`, `task_summary.row` | Within each scrape, grouped rows by year, mileage, price and model string and counted the Craigslist sites per group | **Refuted** | The second dedup key includes `region`, so a truck posted in several sites survives once per site. 4,431 of 61,515 rows with a non-round mileage (7.2%) share year, exact mileage, price and model with a row in another site of the same scrape. Effect: one truck counts twice in a test window and in training. It does not cross the split | SPLIT/dedup; notes must match code |
| 5 | Each scrape is dated by its upload and "holds the listings of about the six weeks before it"; the windows cover "spring 2020 (the market before and at the start of COVID-19)" | `SCRAPE_DATES` comment, `splits_comment` | (a) The builder's listing-id clock (501,677 ids a day, fitted on v8 and v10 posting dates). (b) An independent check: COVID words (covid, coronavirus, quarantine, social distancing) in the posting text of v4–v7, counted only, nothing kept | **Partly refuted** | v8 and v10 hold: their newest posting dates (2020-12-03, 2021-05-05) match the uploads. For v2–v6 the clock puts the newest listing 37–71 days before the upload. The "Mar 2020" window (v5, uploaded 2020-03-22) has 50 COVID mentions in 539,759 adverts (0.01%), rising only in its newest decile. v6 has 1.6% even in its oldest decile. So "Mar 2020" is a pre-pandemic market (Jan to early Mar), and the pandemic's start falls in the "Jun 2020" window. The order of the scrapes holds, so the split and tree models are unaffected; the labels and the splits comment are off | EV-1 |
| 6 | Version 1 is an older scrape, "over a year of postings" before v2, dated 2018-10-10 | `curation_comments`, Assessment | Id clock | Order holds; **date untested** | The clock gives 552 days before v2, but it places v1's listings in Nov 2017–Jan 2018, before the scraper repository existed (2018-09-21). The clock is probably not linear that far back, so the exact date cannot be pinned. v1 is training-only and the date is used only for ordering, so the effect is nil | — |
| 7 | Versions 9 and 10 form one period; no listing appears in two periods | `curation_comments` | Counted listing ids in more than one period of the cleaned frame | Holds | 0 listings in more than one period | SPLIT |
| 8 | Relisted trucks: about 12% (Mar 2020), 17% (Jun), 2% (Sep), 5% (Dec), 3% (May 2021) of each test window; only about 45% of rows carry a VIN | builder issue 3, `curation_comments` | Counted test-window VINs seen in training, and copies on year, mileage, model and site | Holds | VIN relisted 12.3 / 17.5 / 2.1 / 5.2 / 2.9%. Same year, mileage, model and site 11.5 / 18.1 / 2.1 / 4.8 / 2.9%. Same and also the same price 4.4 / 8.2 / 0.9 / 2.0 / 1.3%. VIN share 44–48%. Keeping them is the open issue already in the review | SPLIT-13, LEAK-42 |
| 9 | Training shares 51.6% to 87.8%; five windows; versions 9–10 = 13,239 trucks | `splits_comment` | Read the shipped folds | Holds | Train 55,910 → 95,064 rows; test 13,381 / 10,268 / 6,579 / 8,926 / 13,239 | SPLIT-15 |
| 10 | Down payments posted as the price (under $5,000 for a 2015-or-newer truck) are dropped | `curation_comments` | Looked at the removed rows | Holds | 131 rows, median $2,000; 120 with a clean title, so not salvage trucks | CLEAN |
| 11 | Prices over $150,000 are typing errors | `dataset.py` comment | Listed them | Holds | 60 rows from 157,916 up to 1.1e16; several at 189,000 | CLEAN |
| 12 | Model strings hold no phone numbers | builder checklist | Searched for phone-number patterns | Holds | 0 hits; 16 long strings, all trim and option text | ETH |
| 13 | Version 1 holds 483 Canadian F-150 rows | `curation_comments` | Counted `craigslist.ca` rows with an F-150 model string | **Refuted** (number) | 437 | notes match the data |
| 14 | "Impossible values are set missing": mileage over 500,000 | `curation_comments` | Looked at the low end of the mileage | **Refuted** (incomplete) | Mileages of 0 or 1 on used trucks are kept: 0.2–0.9% of rows have 10 miles or fewer, 66 rows show 1 mile in May 2021, and 0 is the most common value in Dec 2020 (50 rows) | CLEAN |
| 15 | Anomaly: mileage 17–28% missing up to 2020, 1% in 2021 | `curation_comments` | Missing share and price by period; looked for a placeholder fill in 2021 | Holds, and sharper than written | Missing share is 31% (2018), 15–22% (2019–2020) and 0.9% (May 2021), with no placeholder replacing it. In training, a missing mileage marks trucks priced about 0.5 lower in log terms (roughly 40% cheaper). This is the largest drift in the May 2021 window (PSI 0.76) and is probably a change to Craigslist's posting form, which a deployed model would meet too. It is not a defect | DRIFT, EV |
| 16 | No leak; year is the strongest single feature | builder probes | Re-fit LightGBM and ridge per window | Holds | LightGBM RMSE 3,839–6,403 against ridge 6,386–7,804; no near-perfect feature | LEAK |
| 17 | Every feature is known when the advert is written; no gap | implied | Read the columns | Holds | Every feature is an advert field; `scrape_date` is the period stamp | USE |
| 18 | The target is the asking price, not the sale price | `fit_reason` | — | Holds (stated) | | USE-5 |

**Refuted and untested claims, ranked**

1. **Metric (claim 1). Should-level consistency.** The fallback contradicts MET-11's own example and every asking-price or sale-price precedent. RMSE in dollars weights the dearest tenth of trucks at 36–52% of the error.
   - What it changes: the declared metric; the ranking of the two models I fitted does not move.
   - Mildest remedy: `Metric.from_context("rmsle", target_transform="log")` with the immoscout-style reason (the builder's issue 7, option B). Recommend B over the implemented A.
2. **Placeholder regex removes real prices (claim 3). Validity, minor scale (0.4%).** Trucks at $9,999 and at 8,888, 7,777 and 6,666 are removed because of their price.
   - Mildest remedy: take `9999` out of the regex, and limit repeated digits to five or more (11111, 99999) plus the sequences 1234, 12345 and 123456.
   - Then the comment's examples match what is removed.
3. **Duplicates across sites kept within a scrape (claim 4).** The notes and the row description claim one row per truck, but 7.2% of rows with a non-round mileage are the same advert in another site.
   - Mildest remedy: drop `region` from the second dedup key, keeping one row per year, mileage, price and model within a scrape (when mileage is present).
   - Alternative: correct the comment to say the key keeps one row per site.
4. **Scrape-date labels (claim 5).** The listings of v2–v6 are older than their upload dates, so "Mar 2020" is a pre-pandemic Jan to early-Mar market. Neither the split nor the scores change.
   - Mildest remedy: reword the `splits_comment` and the `SCRAPE_DATES` comment to say the uploads lag the listings by up to about ten weeks for v2–v6, and that the pandemic's start falls in the "Jun 2020" window.
5. **Mileage 0 or 1 kept (claim 14).** 0.2–0.9% of rows.
   - Mildest remedy: set a mileage of 10 or less to missing for a truck older than the scrape's model year minus one, and add it to the "impossible values" bullet.
6. **Canadian row count (claim 13).** 483 in the notes against 437 counted. Mildest remedy: correct the number.
7. **Untested: version 1's date (claim 6).** The listing-id clock cannot date it reliably before 2019. It has no effect on the split, which only uses the order.

No finding on the split, the target or a leak beyond the relisted-truck issue the builder already raised; its numbers check out (claim 8).

</details>

<details><summary>Column audit</summary>

I found no column that leaks at the prediction point beyond a dozen model strings that contain the price. I found one cleaning step that doesn't do what the definition says, a platform change that explains the mileage step the builder left unchecked, and a few small cleaning items. The definition's own Kaggle file is not in question: every version is one CSV and all eleven are read.


**Files.** `kaggle datasets files` lists one file for the current version (`vehicles.csv`, v11). Each of the 11 version zips holds one CSV (`craigslistVehicles.csv` in v1–3, `vehicles.csv` after). `_prepare_raw_files` reads all 11, and `curation_comments` says why version 11 is left out. No file is left out without a reason.

**Dtype probe:** 0 of 14 columns flagged.

**Column table (cleaned frame: 108,303 rows)**

| column | meaning (Craigslist advert form / scraper) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| price (target) | asking price at scrape time, log | the outcome | float64 log; 1,000–150,000 plus placeholder filter | fine | CLEAN-16 |
| year | model year | yes (advert) | float64; before 1975 or after scrape year +1 set missing (0.3% missing) | fine | — |
| condition | form option new / like new / excellent / good / fair / salvage | yes | ordinal salvage<…<new; matches Craigslist's scale; 43.8% missing (poster left it blank) | fine | CLEAN-14 |
| cylinders | form option "N cylinders" / "other" | yes | float64, "other" set missing. 219 values are impossible for an F-150 (3, 4, 5, 10 or 12 cylinders) | small cleaning problem | CLEAN-11 |
| fuel | gas / diesel / hybrid / electric / other | yes | category. 11 "electric" trucks of model years 1994–2020, before any electric F-150 | negligible | CLEAN-11 |
| odometer | mileage typed by the poster | yes | float64, over 500k set missing. **547 rows (0.5%) read under 100 miles on trucks at least 2 years old**, peaking at 1.1% in Dec 2020; 66 read "1" in May 2021. **Missing share steps from 13–34% to 0.9%** (see finding 2) | cleaning problem (proxy missing) + note | CLEAN-10; check step 4 |
| title_status | clean / rebuilt / lien / salvage / missing / parts only | yes | category; "missing" is Craigslist's option (no title document), not a missing value | fine (builder's warning answer holds) | CLEAN-10 |
| transmission | automatic / manual / other | yes | category | fine | — |
| drive | 4wd / rwd / fwd | yes | category. **"fwd" on 2,465 rows (2.3%)**: no F-150 is front-wheel drive | cleaning problem (impossible) | CLEAN-11 |
| size | form option | yes | ordinal sub-compact<…<full-size, order right; 61.8% missing; 191 compact or sub-compact (impossible), 1,777 mid-size | fine / negligible | CLEAN-11 |
| type | body type option | yes | category; pickup and truck both used; a few sedan or coupe entries (typing noise) | fine | — |
| paint_color | form option | yes | category | fine | — |
| lat, long | the poster's map pin (or the site's) | yes | float64. ~53 rows outside the US (lat −81, long +37); 964 rows more than 1,000 km from their site's median | small cleaning problem | CLEAN-11 |
| region | Craigslist site, the url's subdomain (413) | yes | category; the same derivation in every version | fine | CLEAN-3 |
| model | the model field as typed (3,377 spellings) | yes | string. **12 rows hold a price or monthly payment ("$21995", "$23,750"); 3 equal the target exactly.** 27 hold mileage ("145k") | weak target-in-feature, negligible | LEAK (target copy), weak |
| scrape_date | upload date of the scrape (time column, also a feature) | yes (a proxy for the posting date, ≤ 6 weeks after it) | datetime | fine | — |
| *(dropped)* vin | 17-character VIN, ~60% of raw F-150 rows, 99.9% Ford-valid | yes, in the advert | dropped as an identifier; chars 5–7 (series/cab/drive, e.g. W1E, X1E, F1C) and char 8 (engine) carry meaning | question for the curator | CLEAN-3, CLEAN-19 |
| *(dropped)* url, id, posting text, title, images, county, state, manufacturer, make, city | identifiers, personal text, constant or empty columns, schema drift | — | dropped, reasons given in `curation_comments` | fine | P1, CLEAN-3, CLEAN-5 |

I ran the timing check (step 2) on every column, and none comes into existence after the advert. No window is computed past the prediction point, no row is overwritten at the end of a period, no value is fitted over the whole release, and no other row's target is stored as a feature. The price is the price at scrape time, so a later edit is possible; that touches the target, not a feature. Relisted trucks across the split are the builder's issue 3 and I don't repeat them.

**Problems, ranked**

**1. The deduplication keeps copies of one truck posted on several sites (P5/P7, plus a note that doesn't match the code).**
- **What the definition says.** `curation_comments` and `row` say "one row per truck within a scrape period … dealers post one truck in several sites", but the key `["scrape_date","year","odometer","price","region"]` includes `region`. So the same truck on several sites stays.
- **How many.** Rows that repeat another row's scrape, model year, mileage (over 1,000) and price on another site:

  | Scrape | Extra rows | Share of the scrape |
  |---|---|---|
  | Oct 2018 to Dec 2020 (each) | 327–665 | 4.0–5.6% |
  | May 2021 window | 1,681 | 12.7% |

  One cluster is 56 sites. The truck at 83,066 miles appears 39 times in May 2021, at prices within 2%. Another 11,779 rows match on scrape, year and mileage but differ in price.
- **Effect.** These copies never cross the split (same scrape), so this is not a leak. Untuned LightGBM, RMSE in dollars:

  | Window | As shipped | Copies dropped |
  |---|---|---|
  | Sep 2020 | 6,442 | 6,427 |
  | Dec 2020 | 4,726 | 4,734 |
  | May 2021 | 5,655 | 5,744 (+1.6%) |

  The copies only over-weight dealers who post widely, mostly in the last window.
- **Mildest remedy.** Either drop `region` from the second key (keep one row per truck, say the first site), or keep it and correct the comment to "one row per truck and site". This is the curator's call. Either way the comment must match the code.

**2. Craigslist made mileage a required field around 30 Nov 2020 (step 4, a partial step the `splits_feature_missing_in_test` warning misses).**
- **Where it shows.** Version 8, read by its `posting_date`: odometer missing in 13.9–16.3% of each week's postings through 23–29 Nov 2020, then 4.5% in the week from 30 Nov.
- **After the change.** Versions 9 and 10 (Apr–May 2021) are 0.9–1.1% missing, and v11 (2026) 0.5–1%. Training is 13–34% missing, the May 2021 test window 0.9%.
- **Side effect.** Placeholder mileages (0, 1) rise right after the change: 1.1% of the Dec 2020 rows on trucks at least 2 years old.
- **Remedy.** This is the data as published and a model in use would meet it, so keep it. Answer the builder's "not checked" in the anomaly line: a Craigslist form change, not the scraper.

**3. Placeholder mileages (P7, CLEAN-10).** 547 rows read under 100 miles on trucks at least 2 years old. Their median price is 12,900, against 16,495 for the other rows, so these are not near-new trucks. Remedy: set an odometer under 100 to missing when the model year is at least 2 years before the scrape year (stated with its count). This mirrors the placeholder-price rule the definition already applies.

**4. Impossible values for an F-150 (P7, CLEAN-11).** About 2,700 rows: "fwd" on 2,465, 219 cylinder counts other than 6 or 8, 191 compact or sub-compact sizes, 11 electric trucks before 2021, and about 53 coordinates outside the US. Remedy: set them missing with a single rule each, rows kept. The cheap ones are `drive == "fwd"`, cylinders not in {6, 8}, and lat/long outside the US. Fine to keep with a note if the curator prefers the poster's input as typed.

**5. The VIN carries meaning that is dropped (P7, CLEAN-3, weighed against minimal preprocessing).**
- **What it holds.** The VIN is in about 60% of raw F-150 rows (41% in v1, 59–67% later), and 99.9% start with Ford's 1FT/2FT/3FT. Characters 5–7 code the series, cab and drive (W1E 62k, W1C 11k, X1E 10.5k, F1C 3.7k), and character 8 codes the engine. That is the cab and engine the model string holds only in its 3,377 spellings, and what a dealer's VIN lookup prices by.
- **The choice.** Keeping two decoded code columns (series/body and engine, as categories with no lookup table) exposes no personal data. Whether to add them is the curator's call; the definition is valid without them.

**6. The target typed into the model field (P4, weak).** 12 model strings contain a dollar amount; 3 equal the asking price exactly, and 9 are monthly payments or down payments. That is 0.01% of rows. Remedy: none needed. Optionally strip `\$[\d,.]+` from `model`.

No other problems found. Every column is known when the advert is written, the ordinal scales run in the codebook's order, and every file of the release is either read or left out with a stated reason.

</details>

<details><summary>Split audit</summary>

The split is **right with notes**. The definition ships the leaf I reached myself, its windows meet the floors, and my checks found no leak along the time order. The notes are about wording in `splits_comment`: what the windows are said to cover, and why there is no gap.

**Walking the tree (SPLIT-36)**
- The record's type is `Dated Event Log`. At **LOG.meets** the use case is later adverts (a seller, dealer or marketplace pricing the next F-150 listings), so the answer is "cases after the data", which leads to the **Order and windows step**. The time key is the scrape.
- **ORDER.order: yes.** The scrape date is recorded per version. I checked it against something it does not depend on: Craigslist listing ids, which follow posting dates with r = 0.99998. Before May 2021 no two consecutive scrapes share any posting time. 0.0% of a scrape's listings have an id below the 99th percentile of the scrape before it. The only overlap is versions 9 and 10 (26% and 62%), which the definition already merges. So every training row was posted before every test row.
- **ORDER.windows: yes.** There are 5 windows of one scrape each, with 51.6% to 87.8% of rows in training. The window length (one scrape) is our assumption, not something the source states, so it needs the curator's sign-off.
- **ORDER.small: no**, because the table is large.
- **Leaf: L-ORDER.windows**, the same as `split_leaf`, the `splits_comment` and the shipped `Temporal(... unit="unique", cutoffs=...)`. No leaf is forced, none departs from the tree, and no question went unanswered.
- Collection facts (`Samples: Over Time`, `Time: Dated`, `Entities: Recur`) match the source.

**Floors and the number of windows (SPLIT-14, SPLIT-15)**
- No window trains on less than half the rows: 51.6, 64.0, 73.5, 79.5 and 87.8%.
- Test windows hold 6,579 to 13,381 trucks, far above 33.
- The target is 9 windows (SPLIT-33, from 108,303 rows); the count is 5, and the 50% floor stops more.
- `dataset windows` agrees: the 5 chosen windows are every eligible scrape, including the newest. The only candidate left out is Jan 2020 at 39.8%.
- No model score picked the windows.

**Ranked findings**

**1. The windows are dated by upload, not by when the trucks were posted (Should, SPLIT-32 time basis / SPLIT-12).**
- Measured posting dates (versions 8 and 10, from `posting_date`):
  - version 8: 28 Oct to 3 Dec 2020 (uploaded 3 Dec);
  - version 10: 4 Apr to 5 May 2021.
- Estimated from listing ids (using the 2020–21 rate):
  - version 9: 17 Mar to 18 Apr 2021;
  - version 7: 1 Aug to 3 Sep 2020 (uploaded 16 Sep).
  - Versions 2 to 6 are uncertain: their estimates end 5 to 10 weeks before the upload. Version 6 ("Jun 2020") would hold postings of about 6 Mar to 10 Apr 2020, and version 5 ("Mar 2020") about 7 Jan to 14 Feb 2020.
- The id-to-date rate drifts between years: about 500k ids a day in 2020–21, 336k a day on average for 2021–26. So the estimates for 2019 to mid-2020 may be off by weeks, and further back version 1 comes out at January 2018, before the scraper's repository existed (21 Sep 2018).
- What it changes: the split itself (the order is checked) is unaffected. But the comment's labels may be wrong: "Mar 2020 … at the start of COVID-19" may in fact be pre-COVID postings, and "Jun 2020" may be March–April 2020.
- **Remedy:** a wording fix only. Say the dates are upload dates. Give the measured posting spans for versions 8 to 10. Drop the COVID and season claims for versions 5 and 6, or flag them as estimates.

**2. The real gaps come from the scrape schedule and are not stated (Should, SPLIT-10 / SPLIT-12).**
- By listing id, the time between the newest training posting and the first test posting is about:
  - Mar 2020: 7 weeks
  - Jun 2020: 3 weeks
  - Sep 2020: 16 weeks
  - Dec 2020: 7.5 weeks
  - May 2021: 15 weeks (measured from the version 8 dates)
- "No gap" is right for the label: the price comes with the advert. But the tests are harder than a model refit monthly would face. The builder's "5 to 21 weeks" is the spacing of upload dates, not of postings.
- **Remedy:** state these gaps in the splits comment and the horizon block. No re-split.

**3. Relisted trucks cross the split (note; SPLIT-13, LEAK-42/43).**
- 8.0% of rows are relistings linked by VIN: 2% to 17% of a test window. Only 45% of rows carry a VIN at all.
- In 3 of 5 windows the relisted trucks are priced more accurately than fresh ones, so an earlier listing acts as a near-copy.
- Dropping them moves the error by −1.6% to +1.9%.
- Keeping them is consistent with a use case of known trucks, and the definition says so as a "kept on purpose" leak. This is the curator's call, already raised as builder issue 3; I add nothing new.

**4. The newest window is complete, but one column changes inside it (note).**
- The May 2021 window is not cut short: about 270 rows a day against about 230 in Dec 2020.
- The price rise matches the 2021 used-truck market, not a scrape cut.
- But odometer missingness falls from 17–28% to 1% in May 2021 (drift score 0.76). This is a change in how the data was collected, inside the deployment window. It is tested, which is right; the column auditor should confirm the cause.

**5. The date of version 1 is uncertain (note).** Its dating to 2018-10-10 is not confirmed, and the listing-id estimate says early 2018. It is used for training only and is the oldest scrape either way, so the split does not change.

**Horizon block (for the curator to sign off)**
- **Verdict:** right.
- **Length:** one scrape, about 5 weeks of postings; 7 weeks for the merged May 2021 scrape. The source states only that the data was scraped "every few months". That the refit step equals the scrape is our assumption.
- **Gap:** none for the label (the price arrives with the advert). The scrape schedule leaves 3 to 16 weeks unobserved before each test window.
- **Time frame:** postings from about Jan 2020 to May 2021: winter 2020, spring 2020 (around the COVID start, estimated), Aug 2020, Nov 2020, and spring 2021 when prices rose.

| Option | Windows | Train share | Test sizes |
|---|---|---|---|
| A: one scrape (implemented) | 5 | 51.6–87.8% | 6,579–13,381 |
| B: A plus Jan 2020, as the curator's exception | 6 | 39.8% for the new window | +12,831 |
| C: versions 9 and 10 as separate windows | — | — | they overlap in posting time and share 26% of listings, so not one-unit windows |
| D: cut inside each scrape by listing id | — | — | the early postings in a scrape are the ones still unsold at scrape time, so the cut mixes in that selection |

Recommendation: **A**. Option B adds only another pre-COVID winter, which the Mar 2020 window already covers.

I did not need to fit a model under another split. The builder's comparison (earlier scrapes vs a random split within the scrape: the error is higher by up to 19% in the three newest windows and lower in the two older ones) already backs the temporal regime.

</details>

<details><summary>Domain practitioner</summary>

I would use this model, with two changes. The task is real: an F-150 seller, a dealer or a marketplace sets or judges an asking price from what the advert shows, against earlier listings. Two inputs that every Craigslist advert shows are dropped, and adding them back cuts the RMSE by 7 to 11% in every window.

**Fit: **approximate** (I agree with the definition, for a different reason)**

The data is real Craigslist listings, tested on later scrapes. But the poster writes the advert title and picks the owner or dealer section, and the shipped columns keep neither.

The definition's `fit_reason` names other gaps, and two of them are not gaps:
- **Asking price, not sale price.** For the seller and the marketplace this is not a gap (USE-5, USE-9). The asking price is the number the seller sets. Marketplace price guides are built from listings: CarGurus calls its Instant Market Value "an estimated fair retail price … based on … comparable current and previous car listings", recomputed daily. Its deal ratings compare a listing's asking price to that value. Only a buyer who wants the final sale price meets a real gap.
- **The relisted trucks.** These are a leak kept on purpose. By USE-8 they are named as kept, not as a gap in the fit. `fit_reason` lists them as a gap and should be reworded.

**The gaps, ranked by how much they change the task**

1. **The advert title is dropped, though it is in the data and carries no personal data.**
   - Craigslist urls carry the title as a slug: `/cto/d/el-paso-2012-ford-f150-v8-50l-4x4-4/…`. 99.9% of rows have one.
   - 59% of F-150 rows have a bare model string ("f-150" or "f150"). In 51% of those, the slug names the trim (raptor, lariat, platinum, king ranch, xlt, crew, 4x4…).
   - No slug holds anything that looks like a phone number. The definition drops the url only as an identifier, and the title text was never read, for phone numbers that sit in the body text.
   - The largest test errors (May 2021) are almost all real high-end trucks listed with a bare "f-150": 70,000 to 140,000 dollars against a prediction of 30,000 to 43,000. The slug would show those trims.
   - Adding about 27 trim and cab flags from the slug, plus the seller type, lowers the RMSE in every window:

     | Window | RMSE now | RMSE with slug and seller type |
     |---|---|---|
     | Mar 2020 | 3,905 | 3,521 (−9.8%) |
     | Jun 2020 | 4,084 | 3,660 (−10.4%) |
     | Sep 2020 | 5,936 | 5,488 (−7.5%) |
     | Dec 2020 | 5,121 | 4,601 (−10.2%) |
     | May 2021 | 6,307 | 5,880 (−6.8%) |

     RMSLE drops 3.5 to 4.4% (untuned LightGBM, the builder's settings).
   - As a pricer, the title is the first thing I read: it is where posters write the trim, the cab and words like "lifted". Without it the task is to price a truck while hiding the advert's headline (USE-6: anything known at the prediction point is a legitimate input).
   - **Change:** ship the slug, with the city prefix stripped, as a second `string` feature, or a trim parsed from slug plus model string.

2. **Owner or dealer is dropped, though it is in the url.**
   - Every url has `/cto/` (by owner, 38,073 rows) or `/ctd/` (by dealer, 70,230 rows). The poster picks the section, and the buyer and the seller both see it.
   - Comparable trucks (2013-2015, 60,000 to 120,000 miles) are listed 500 to 2,200 dollars higher by dealers in every scrape. Example: 26,000 against 23,800 in May 2021.
   - Dealer rows are also 55% missing `condition`, against 23% for owners. Missing fields mean different things for the two groups.
   - On its own the seller type gains little: −0.2% to −0.7% RMSE, because year and mileage already separate the groups. It still belongs in the task because every actor has it.
   - **Change:** ship `seller` (owner / dealer) as a categorical feature.

3. **The horizon is longer than in practice.**
   - A seller or marketplace prices against today's comparables, refit daily (CarGurus). Here the test scrape is 5 to 21 weeks after the training data, across the 2020-21 rise in used-car prices.
   - So the 9-19% gap between the later-window error and a random split within the same scrape partly measures a refit delay no practitioner has.
   - The split is still honest (later market, no look-ahead). It cannot be shortened: the posting date exists in only some versions. This is something to name in `fit_reason`, not to fix.

4. **A scrape catches the stock of open listings, not the flow of new ones.**
   - Trucks that sit unsold for long, often the overpriced ones, are more likely to be caught by a scrape.
   - Small and shared by every listing-based price guide, so it is a note, not a change.

5. **Fields the poster types in (condition, size and so on 20-75% missing).** This is what a marketplace meets, so the data mirrors it and there is no gap.

**The five questions as the actor**

1. **Inputs.** Everything shipped is known when the advert is written. Missing although I would always have them: the title (gap 1), owner or dealer (gap 2), and the photos and body text (fairly dropped). Nothing shipped is unknown at that moment. I see no leak beyond the relistings the builder already named; keeping them fits a dealer who knows his earlier price (SPLIT-13, USE-10).
2. **Target.** The asking price is what I set or judge, and I want a number in dollars. It is not a proxy, except for a buyer who wants the sale price.
3. **Rows and test data.** One row is one advert, which is one pricing decision. A later scrape is the next market, which is the right test.
4. **Would I use it?** Yes, as a comparable-based price guide. Trust would come from per-trim accuracy. I would distrust it on high-end trims (Raptor, Shelby, Platinum) while the title is missing, because that is where today's largest errors are.

**Metric: **partly****

Declared: RMSE in dollars after the inverse of the log target (fallback, MET-1, MET-3; no source metric, and the reason recorded is fine).

- **What it gets right.** A dealer thinks in dollars, so a dollar error is a fair unit, and the unit is the listing I price (MET-1).
- **What is off.** A pricer judges error relative to the truck's value: 3,000 dollars off a 6,000-dollar truck is a mispriced advert, 3,000 off a 45,000-dollar truck is noise.
  - RMSE in dollars is driven by the expensive, poorly described trucks and by the remaining odd prices. The worst 1% of test listings carry 26-31% of the squared error in every window.
  - In May 2021, listings priced under 30% or over 2.5× the prediction are 1.5% of rows but 11% of the squared error (RMSE 6,307 with them, 5,983 without).
  - So the model I would pick by RMSE in dollars is mostly the one that guesses the outliers and the premium trims.
- **What I would choose.** RMSLE on the dollar price: `rmsle` with `target_transform="log"` under MET-3. It scores relative error, the way price guides and deal ratings judge it ("x% above market"). It is the price-regression convention in the collection (diamonds, mercari_price_suggestion, california_house_prices_2020). It weights a cheap old truck and a new one alike, and depends less on the few remaining typo prices.
- Keeping RMSE in dollars is defensible (a dealer's gross margin is in dollars). Choosing between them is a MET-10 weighing call for the curator, including the diversity factor. Neither is wrong, but RMSLE fits the decision better.

**What a used-vehicle pricing expert would change**

- Ship the title slug, or a trim and cab parsed from it plus the model string, and the owner/dealer flag. These are the two inputs anyone pricing a truck reads first (gaps 1 and 2).
- Reword `fit_reason`: the asking price is the target for the seller and the marketplace (it is a gap only for a buyer who wants the sale price). Name the relistings as a kept leak, not a gap. Add the long horizon.
- Consider RMSLE as the metric (above).
- Keep the 2026 scrape out, and keep the relisted trucks with the note as written.

**Sources**

- The data: the definition's Ford rows (url segments `/cto/` and `/ctd/`, and the slug after `/d/`), cleaned with the definition's own `_clean`.
- The builder's report and probes; the record's screening block; fiat_500's review.
- CarGurus on its Instant Market Value: [cargurus.ca help thread](https://www.cargurus.ca/Cars/Discussion-t29605_ds1140402), [how IMV is calculated](https://cargurus.ca/Cars/Discussion-t23322_ds536763), [CarGurus car valuation](https://cargurus.com/research/car-valuation). One poster in the first thread saw a dealer car valued about 2,000 dollars above the same private-sale car.
- Craigslist sections: no page defines the codes. That `ctd` is the dealer section and `cto` the owner section is inferred from [a dealer listing under /ctd/](https://hartford.craigslist.org/ctd/d/meriden-1991-dodge-dakota-one-owner/7896595171.html) and [craigslist /cto/ pages](https://www.craigslist.org/about/best/all/cto/). It also fits the data: newer, cheaper-per-truck-age listings sit under `/ctd/`.
- Rules: USE-5, USE-6, USE-8, USE-9, USE-10, SPLIT-13, MET-1, MET-3, MET-10. MET-6 to MET-9 cover probabilities and thresholds and do not apply to this regression.

</details>

<details><summary>Precedent check</summary>

I checked 13 of the builder's calls against earlier decisions. Two depart from them without a stated reason, one leaves a dependency out of its issue, and the other ten follow precedent. I edited nothing.

**Precedent check: craigslist_used_vehicles_f150 (AI, 2026-11-25)**

**Findings, most important first**

**F1. Metric (builder's issue 7, recommends A, the fallback `rmse`): departs with no stated reason**
- **Precedents:** every other asking-price or sale-price task with a log target is scored by `rmsle` from context:
  - diamonds (Lennart, 2026-10-21) set the rule's own example under MET-11: "a price's error matters relative to the price, so `rmsle` on the price in dollars".
  - perth_house_prices, scraped listings, checked by Lennart on 2026-10-26.
  - immoscout_german_house_prices: "For an asking price the error that matters is relative to the price". This is the closest case, a scraped asking price.
  - Also house_sales, melbourne_housing_market, wine_world_cost, mercari_price_suggestion and california_house_prices_2020, the last two with `rmsle` as the source's metric.
  - Only fiat_500 uses the fallback `rmse`, and it ships the raw price without a log.
- **Why it applies here:** prices run from $1,000 to $150,000, the median is about $15k–26k, and the 2018 scrape's median is $9,500. So a $3,000 miss means very different things across rows. That is the condition MET-11 `context` names.
- **What the builder says:** issue 7 calls B "defensible with precedent" but gives no fact that sets this case apart for A.

> **Score the F-150 asking price by RMSLE, as every other price task, or by RMSE in dollars?**
>
> * **Problem:**
>   - The definition uses the fallback RMSE in dollars on a log target. Every other price task with a log target uses `rmsle` from context, including diamonds, which set the rule, and immoscout, also scraped asking prices[^m11].
>   - Prices span $1,000 to $150,000, so the error that matters is relative to the price. That is the case MET-11 `context` was written for[^m11].
>   - No fact in the notes or the issue sets this dataset apart.
>
> | | Option | Pro | Con |
> |---|---|---|---|
> | a | Keep `rmse` in dollars, recorded as an exception. Best guess at the fact: "a seller's loss is in dollars, and an F-150's prices are narrower than houses or diamonds" | follows fiat_500, the dataset it replaces | the price range is still 150×; it would be the only log-target price task off `rmsle` |
> | b | `Metric.from_context("rmsle", target_transform="log")`, as diamonds and immoscout | treats like cases alike; LightGBM RMSLE is 0.30–0.34 | none found |
> | c | Reopen diamonds and the house-price tasks to match | — | overturns curator decisions with no new fact |
>
> **Recommendation:** b.
>
> [^m11]: MET-11 (Must) `context` (Lennart, 2026-10-21, diamonds); MET-3.

**F2. One row per truck within a scrape: the dedup key does not do what the notes say, and departs from fiat_500**
- **The gap between note and code:** the notes say "one row per model year, mileage, price and Craigslist site (dealers post one truck in several sites…)". But the key includes `region`, so a truck posted in several sites stays once per site.
- **Measured on the cleaned table, 108,303 rows:**
  - 4,431 of 61,515 rows with an odd mileage (not a multiple of 1,000) share scrape, model year, mileage, price and model string with a row from another site.
  - Another 1,787 odd-mileage rows match scrape, model year, mileage and model string at a different price.
  - The table holds 2,707 rows that are identical in every shipped field but differ in price (the builder's 1,495 likely counts the extra rows only). Only 51% of them carry a mileage, so many may be different trucks.
- **Precedent:** fiat_500. Lennart decided on 2026-10-14 to keep one row per car, with a key without price or place (the same car at several dealers is one car). fiat_500's own issue 1 recommends matching on odd mileages.
- **A fact that may set this case apart, not written down anywhere:** under the split by scrape, every copy sits in the same scrape, so on one side of the split. No copy crosses from training to test, unlike fiat_500's random split. The copies still weight multi-site dealers more in training and count one truck several times in the scored test window.

> **Drop a truck posted in several Craigslist sites within one scrape down to one row, as fiat_500 keeps one row per car?**
>
> * **Problem:**
>   - The notes promise one row per truck, but the key keeps a truck once per site: 4,431 odd-mileage rows (7.2%) repeat a truck's year, mileage, price and model string in another site of the same scrape[^c].
>   - fiat_500 drops these copies whatever the place[^p].
>   - They never cross the split (same scrape), so the cost is weighting and double scoring, not a leak.
>
> | | Option | Pro | Con |
> |---|---|---|---|
> | a | Keep as is, as an exception. Fact: "copies stay within one scrape, so on one side of the temporal split"; reword the note | no rows lost | a test window scores some trucks several times; the note no longer matches the code |
> | b | Drop `region` from the key for odd mileages (one row per truck), as fiat_500's issue 1 B | one truck, one row, as fiat_500 | the site kept is arbitrary (keep the last, as now) |
> | c | Treat fiat_500 like this (reopen) | — | fiat_500 has a random split, where copies do cross |
>
> **Recommendation:** b, or a with the note corrected.
>
> [^c]: CLEAN-1; minimal preprocessing.
> [^p]: fiat_500 CC (2026-10-14, Lennart); LEAK-42.

**F3. Issues 1 and 2 depend on each other, and issue 2 does not say so**
- **Measured:** without version 1, the Mar 2020 window trains on 42.9% instead of 51.6%. That is below SPLIT-14's 50% floor (a Must), so the window would need the curator's exception. The other windows would train on 57.5%, 68.7%, 75.8% and 85.6%.
- **Why it matters:** version 1's date (2018-10-10) is inferred from the order of listing ids, which is a measurement, plus the first upload date, which is an inference. That version is what lets the fifth window clear the floor.
- **What issue 2 says now:** only that dropping version 1 moves the RMSE by −1.6% to +1.5%. Its option B needs to say "and Mar 2020 falls to 42.9% (curator's exception, or 4 windows)".
- **Related tag:** the record's tags say `Time: Dated` only. If the curator relies on version 1, it may need `Time: Inferred` for that period (diabetes_130_us used the tag, 2026-11-11). This is a question for the record, not a departure.

**Decisions that follow precedent**

| Decision | Verdict | Precedents |
|---|---|---|
| Windows A: 5 windows, all ≥50%, Jan 2020 (39.8%) not taken | Consistent with SPLIT-14 as amended on 2026-11-11. Curators often accept windows under 50% when the review offers them (anes_voting_2026 down to 40.0%, mercedes_benz down to 31.5%, ieee 38.9%, maps_router_eta 44.8%; Lennart, 2026-11-11), so the issue should list them beside option B. Jan 2020 adds little the Mar 2020 window lacks (both before COVID; Dec 2020 is the winter window). | splits.md Cases rows for SPLIT-14 |
| Relisted trucks kept across scrapes (issue 3 A) | Consistent, with a stated reason. What sets it apart from melbourne's within-60-day merging: a relisting is a new advert at a new price in 61.5% of cases, not the same event reported twice. Suggest a LEAK-42 / SPLIT-13 Cases row. | house_sales (resales kept as history under the temporal split), melbourne_housing_market (resales 63+ days apart kept), liberty_mutual_fire_peril_loss_cost (renewals of known risks kept), diabetes_130_us (returning patients, Andrej, 2026-11-11) |
| 2026 scrape left out (issue 4 A) | Departs from g_research, with stated reasons: a five-year gap breaks the one-scrape horizon (SPLIT-12), and the 2026 file has its own columns. Reasonable; not a breach of SPLIT-15's newest-window Must, which applies to the release the task is built from. | g_research_crypto_forecasting_1m (newer months appended, Lennart, 2026-11-11: they continue the release minute by minute) |
| Placeholder and down-payment prices dropped (issue 5 A) | Consistent | mercari_price_suggestion ($0 dropped, Andrej, 2026-11-09: "no sale is free"), immoscout (under €10k, "price on request"), house_sales (non-market sales dropped) |
| Model string shipped as text (issue 6 A) | Consistent: a fixed trim list would be a feature of our own invention, which CLEAN-19 does not cover | mercari keeps the item name as text |
| Split leaf L-ORDER.windows, no gap | Consistent | house_sales, melbourne_housing_market, perth_house_prices |
| Domain `business & marketing` | Consistent | fiat_500 CC (Andrej, 2026-11-05) |
| `year` 2018, `original_source` Kaggle (PROV-9, PROV-8) | Consistent | — |
| One-model filter treated as the population, not a selection bias | Consistent: same pattern as fiat_500 | — |

**Drift and repeated exceptions**
- **Drift:** none found on the rules touched here. Every curator decision on price metrics since 2026-10-21 chose `rmsle`.
- **Third exception:** none due. The exceptions under 50% on SPLIT-14 were already turned into the 2026-11-11 amendment, and this definition takes none.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** This is a real and useful task: pricing used Ford F-150s from Craigslist listings, split by time. But the table should be deduplicated across scrapes, and the target should be documented as log asking price, trimmed to $1,000–$140,000.

**What the task is.** A seller, a dealer or a valuation tool estimates the asking price of a used F-150 from its listing details. A buyer can use the same estimate to spot good or bad offers. That is a real, common use. The table has 108,303 rows from 9 scrape dates, from 2018-10-10 to 2021-05-06. The temporal split on `scrape_date` matches how such a model would be used: fit on past listings, price new ones.

**Concerns, most serious first**

1. **The same listing appears in several scrapes, so some test rows also sit in training.**
   - The table merges 9 snapshots. The README calls the source scraper one that "scrapes used vehicle listings weekly from all regional Craigslist sites", and listings stay live or get relisted.
   - The listing id, URL and VIN were all dropped, so exact deduplication is no longer possible.
   - No rows are exact duplicates. But 8,263 rows repeat an earlier row on every feature (date ignored), and 3,009 also repeat the price.
   - Share of test rows that match an earlier training row on all 15 features:
     - 2020-03-22 window: 12.3% (8.9% when odometer is present, so the match is very likely the same truck)
     - 2020-06-17 window: 20.1% (16.0%)
     - The later three windows: 1.5–2.8%
   - This makes the first two test windows look easier than they are.
   - **Fix:** deduplicate on VIN or listing id from the raw data and keep the first sighting. Failing that, drop later rows that match an earlier one on all features plus price, at least where odometer is present.

2. **The target is not what its name suggests.**
   - `price` is the natural log of the asking price, not a sale price. Its values run from 6.91 to 11.85, which is exp() = $1,000 to $139,977.
   - The hard floor and ceiling show that someone trimmed the target. The scraper itself only skips listings with no price, so the cuts were made during preparation.
   - Placeholder and junk prices are likely still there. Round numbers dominate: $2,500 (1,109 rows), $3,500 (1,101), $4,500 (1,017).
   - **Fix:** state the log transform and the trim in `task.md`. Consider a less arbitrary rule for removing placeholder prices than a flat $1,000 floor.

3. **There is real price drift over time.**
   - Median price by scrape: $9,500 (2018-10), about $14,500–15,300 (2019-10 to 2020-06), then $18,500–19,500 (2020-09 onward). The jump matches the 2020–21 used-car price surge.
   - The 2018 snapshot also sits a year apart from the others and has a much lower median.
   - This is honest temporal shift, not a flaw, and it makes the test harder. Keep it, but describe it in `task.md`.

4. **There is clear signal, but one feature carries most of it.**
   - LightGBM on the expanding-window split scores R² 0.83–0.87 and MAE 0.20–0.24 in log units. Predicting the training median gives MAE 0.62–0.75.
   - `year` accounts for 82% of the model's split gain, `odometer` for 5% and `region` for 4%.
   - The task is not trivial, and at 108k rows it is large enough to score. Model differences may be small, though, because year and mileage do most of the work.

5. **Data quality: the rows look real and scraped, with typical Craigslist mess.**
   - Coordinates: some rows have impossible values for their region, for example lat −51.5 for `losangeles` and lat −12.7 for `anchorage`. Set these to missing.
   - Odometer: 269 rows have 0 and 695 have less than 100.
   - `type` contains labels that cannot fit an F-150: sedan (115), coupe (11), hatchback (5).
   - Missing values are high: `size` 62%, `condition` 44%, `cylinders` 36%, `paint_color` 31%, `type` 30%, `drive` 24%.
   - `model` is free text with 3,377 distinct values. "f-150" and "f150" are spelled both ways, and trim names (xlt, lariat) are buried in the text.
   - Column types are sensible: categories are stored as category, and `model` is kept as a string. Leaving `model` as raw text is acceptable and makes the task a realistic high-cardinality test.

6. **No column leaks the target.** Everything in the table is known when the listing is posted. The free-text description, which can state the price, was dropped. That is good.

There is no training-weight column, so there was nothing to judge on that point.

**What I could not check**
- The Kaggle page returned only its title, so I could not read the version history. I could not confirm that `scrape_date` corresponds to the Kaggle dataset versions, how the rows were narrowed to F-150s, or where the $1,000/$140,000 trim came from.
- Without VINs or listing ids I could not measure the true number of duplicate listings. The feature-match counts above are approximate: they include some different trucks that happen to look identical and miss relists whose details changed.
- The source does not say outright that the price is an asking price. I inferred it from how the scraper records it: the price shown on the listing, with "$" and commas removed.

I opened no files outside the clean room.

</details>

<details><summary>Task gamer</summary>

**Craigslist used Ford F-150 asking price: how far the task can be gamed**

**Verdict:** the task can barely be gamed. The only gain beyond noise comes from the same truck appearing in earlier scrapes, worth about $40 of RMSE on average (0.9%), mostly in one window. The bigger issue cuts the other way: the oldest training rows and the default log-scale fit hurt an honest model by about $270.

The metric is RMSE in dollars. `score()` exponentiates the log price before computing it. Every model below is LightGBM (500 trees, learning rate 0.05, 63 leaves), scored on all 5 shipped windows. Three reference scores:
- **Baseline B:** `features()` with the log target. Mean RMSE **$4,918**; per window (r0…r4) 5656 / 4719 / 6418 / 3953 / 3842.
- **Honest H:** the dollar target, an age feature (scrape year minus model year), keyword flags from the `model` text (raptor, platinum, lariat, …) and only the last 5 scrape dates for training. Mean **$4,646**; per window 5432 / 4579 / 5841 / 3718 / 3661.
- **Noise:** adding a random column moves the score by $8–47 per window; the mean moves by $8 against B and $15–22 against H.

**Exploits**

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Price of the same vehicle in an earlier scrape (exact match on all features, or on year, odometer, model and lat/long) | measured | H 4646.1 / B 4917.7 | 4604.1 / 4872.2 | vs H: +5 to +129 (mean +42); vs B: −2 to +146 (mean +45) | Partly. Relists of a truck at its earlier price are real history. But a row in two scrapes is often one listing that was still live, so it was posted before the cutoff | Keep only each listing's first appearance across scrapes, or drop test rows already seen in training |
| 2 | Counts over the whole table: copies of the same vehicle within a scrape (test rows included), across all dates (later scrapes included), and listings per lat/long | measured | B 4917.7 | 4903.3 | −2 to +28 (mean +14), at the edge of noise | No: these counts use test and later rows | None needed |

**1. Same truck in an earlier scrape**
- **Mechanism:** some test rows are exact feature copies of training rows: 1.5–2.8% in windows r0–r2, 20% in r3 and 12% in r4. On the looser key (year, odometer, model, lat/long) the share is 2–25%. Only about 40–50% of these copies carry the same price.
- **Where the gain is:** the earlier price as a feature helps almost only in r3 (test scrape 2020-06-17, previous scrape 2020-03-22): +$129 against H, +$146 against B. Elsewhere the gain is $5–37, near the $8–47 noise.
- **What would decide it:** the original `posting_date` or listing `id`. If the copies are the same listing, posted before the cutoff, this is leakage from listings that persist across scrapes. If they are reposts, it is legitimate history.
- **Mildest fix:** deduplicate across scrapes, keeping the first appearance.

**2. Counts over the whole table**
They add $14 against B, which is about noise. Not worth fixing.

**A flaw that hurts the honest model**

| Flaw | Honest choice | Baseline | Honest | Gain | Fix |
|---|---|---|---|---|---|
| The training set includes the 2018-10-10 scrape and the log-scale fit does not suit a dollar RMSE | Fit on dollars, add age and `model` keywords, and train on the last 5 scrape dates only | 4917.7 | 4646.1 | −73 to +577 per window (r2 +577, r0 +225 with recency) | Say in `task.md` that the metric is RMSE in dollars, and drop or down-weight the 2018 scrape |

- **Stale year:** the 2018-10-10 scrape holds 16.5k rows with a mean price of $13.4k, against about $16–17k for 2019–2020 and $21k from September 2020 on. Used-truck prices jumped in late 2020 and 2021, and the trees cannot extrapolate past the last training date.
- **Window bias:** the dollar-fit model's mean error is +$2,965 on r2 (2020-09-16) and +$1,460 on r0 (2021-05). Scaling predictions by 1.10–1.15 would cut r2 from 6,072 to about 4,936. But that factor needs the test labels, so it is not usable. It only shows the error is mostly a level shift per window.
- **Fitting on dollars** alone gives 4,795 against 4,918, because `exp` of a log-scale prediction is the median, not the mean.

**Attacks that found nothing**
- **Format-only features** (missing-value flags, odometer round to 100 or 1,000, odometer last digit, lat decimals, `model` string case, dashes, length): RMSE 12,200. That is useless; for scale, predicting the training mean in log space gives 17,277 on r0.
- **Number precision:**
  - `odometer`, `year` and `cylinders` are all whole numbers.
  - Lat/long decimals vary by scrape date: about 3.9 for 2020-01 to 2020-09, about 5 elsewhere. That is a scraper change, so it only tracks the date and says nothing about price.
- **Odometer below 1,000** (1.5% of rows, median $9k against $15k): a real listing artefact the seller types in, so it is signal, not a leak.
- **Nearest training row's price** (on lat/long, year and odometer): mean 4,667 against H's 4,646, so worse overall. It gains on r3 and r4 and loses on r0–r2.
- **Training rows dated at or after the prediction point:** none. Every training date is earlier than its test date, and each test window is a single scrape date.
- **Later records of the same unit in training:** impossible here, because all training rows come earlier.
- **Weight:** the task has none.
- **Columns from after the prediction point:** none of the remaining columns obviously post-dates the posting.
- **Transforms over all rows** (z-scores, min-max, ranks): none present.
- **Label-based selection:** the price floor of $1,000 and cap of about $140k apply to both sides, so they do not distort the split.

**What I could not check**
- **Relist or still live:** without `id`, `url`, `VIN` or `posting_date`, I cannot tell whether a cross-scrape copy is one listing still live or a new post. These columns are in the Kaggle source and were dropped from the kit.
- **Same truck in several regions:** I could not check whether dealers post one truck in several regions within a test scrape. Exploiting that would need test labels anyway.
- **Source file:** I did not download the published Kaggle file. Looking rows up in it would work, since every public dataset allows that, and I have not ranked it.
- **Web sources:** I found no leak or "magic feature" threads for this dataset. One project notes exact duplicate rows ([Medium](https://medium.com/swlh/exploring-and-analyzing-used-car-data-set-2e2bf1f24d52)). The [OpenML listing](https://api.openml.org/d/43305) says older versions of the dataset hold previous listings, which fits the cross-scrape copies above.


Sources:
- [Exploring and Analyzing Used Car Data Set (Medium)](https://medium.com/swlh/exploring-and-analyzing-used-car-data-set-2e2bf1f24d52)
- [OpenML dataset 43305](https://api.openml.org/d/43305)
- [CMU capstone analysis](https://stat.cmu.edu/capstoneresearch/fall2022/315files_f22/team11.html)

</details>

<details><summary>Advocate</summary>

**Advocate opening brief: `craigslist_used_vehicles_f150`**

**Verdict:** ship after a few changes to the definition. Every validity Must holds: the use case is real, the split is right, and the leak is small and kept on purpose under a rule. The real problems the panel found are the metric and some cleaning (P6 and P7). Each is fixed by editing `dataset.py`, the mildest step on the remedy ladder. None calls for dropping the dataset.

**1. The task is real. It is also the only data that meets the curator's ask, which is why it replaces `fiat_500`.** (P3 · USE-1, USE-5 Must · TP-6 Must)
- **The actor:** the domain practitioner would use the model "as a comparable-based price guide". The blind reviewer, who had none of our notes, calls it "a real and useful task".
- **The target is what the actor acts on (USE-5).**
  - The asking price is the number a seller sets and a marketplace judges.
  - Marketplaces build their price guides from listings: CarGurus' Instant Market Value is "based on … comparable current and previous car listings".
  - The asking price differs from the sale price only for a buyer who wants the final sale price. That gap is already stated as fit "approximate".
- **No better data exists:**
  - fiat_500's review compared eight downloaded used-car tables plus the 2026-11-25 searches. No other public table has dated, repeated scrapes of one model.
  - `fiat_500` is one crawl of 1 April 2020 (1,434 cars). It cannot test a later market.
  - This dataset has 108,303 trucks over nine scrapes.
- **Why it outranks the objections:** the objections below are all P6 or P7. P3 ranks above them. Under the "real task against imperfect cleaning" tension, the task stays and the cheap fixes are made.

**2. The split matches the application, and the panel found no leak along the time order.** (P4 · SPLIT-14 Must · SPLIT-36)
- The split auditor walked the decision tree on its own and reached the same leaf, L-ORDER.windows.
- Craigslist listing ids follow posting dates (r = 0.99998). By those ids, 0.0% of a scrape's listings come before the 99th percentile of the scrape before it. Every training row was posted before every test row.
- SPLIT-14 holds:
  - 5 windows, training on 51.6%, 64.0%, 73.5%, 79.5% and 87.8% of the rows;
  - test windows of 6,579 to 13,381 trucks;
  - `dataset windows` confirms these are all the eligible scrapes.
- The task gamer: "the task can barely be gamed." Format artefacts, row order and statistics over all rows gained nothing above noise.
- **What I concede:**
  - The windows are dated by upload, so "Mar 2020 … start of COVID-19" is wrong. The claim and split auditors estimate that version 5 holds roughly Jan to mid-Feb 2020 postings. The comment should also state the 3 to 16 weeks the scrape schedule leaves unseen before each window.
  - These are wording fixes to `splits_comment` (EV-1). The split auditor confirms the order, the folds and the scores do not change.
- **Version 1's date** is inferred (precedent F3). The split uses only the order, and the order is measured from ids, so the inferred date is enough. If the curator wants, tag that period `Time: Inferred`, as was done for diabetes_130_us.

**3. Keeping relisted trucks is the temporal fix LEAK-42 prescribes, not a leak left in by mistake.** (P4 · LEAK-42 Must, verdict 3 · SPLIT-13 Should)
- **The rule:** LEAK-42 verdict 3 says a temporal split fits "when the use case sees the unit again at prediction time (a renewal, a repost the moderator has seen)". That is this case. A dealer knows the earlier price of a truck it posts again (SPLIT-13, USE-10).
- **The fact that answers the blind reviewer and the task gamer:** both feared a cross-scrape copy is one listing still live from before the cutoff. They could not check, because ids were withheld from them.
  - The claim auditor counted **0 listing ids in more than one period** (claim 7), and the split auditor found no id overlap between consecutive scrapes.
  - So every relisting is a new advert. In 61.5% of cases it is at a new price.
- **Size:**
  - Dropping the linked relistings moves the RMSE by −1.6% to +1.9%.
  - The task gamer's best exploit using them gains $42 on a mean RMSE of $4,646 (0.9%). Per-split noise is $8 to $47.
- **Precedents:** house_sales, melbourne_housing_market, liberty_mutual and diabetes_130_us all keep returning units under a temporal split (precedent checker: consistent).
- **Remedy:** a note, already written ("Potential leak, kept on purpose"). The domain practitioner rightly asks that `fit_reason` name it as a kept leak rather than a gap in the fit (USE-8). That is a wording fix.

**4. The task is worth benchmarking: it has signal, it is not solved, and it separates methods.** (P6 · TP rules)
- Dummy RMSE 14,725. Linear model 5,983 (R² 0.777). LightGBM 4,842 (R² 0.867). LightGBM beats the linear model by +0.089 R² (paired SE 0.004).
- Trained on earlier scrapes, LightGBM errs 15% to 25% more than a random split within the same scrape shows. The time component is real.
- Model year carries 82% of the split gain, but without it R² is still 0.632. The 3,377 model-string spellings and the 2020-21 price drift make the task hard.
- The drift (median $14.5k in 2019-20 to $18.5k-19.5k from Sep 2020) is honest temporal shift. The blind reviewer: "keep it". The task gamer's down-weighting of the 2018 scrape is a modelling choice for participants, not a defect (P4 over P6).

**5. The metric: I concede. Switch it to RMSLE with one line.** (P6 · MET-11 Must, MET-3 Must)
- MET-11's own example of a `context` metric is "a price's error matters relative to the price, so `rmsle`".
- Every other price task with a log target uses it: diamonds, immoscout (also a scraped asking price), perth, house_sales and others. Nothing sets this dataset apart (precedent F1).
- The 10% dearest trucks carry 36-52% of the squared dollar error.
- **Fix:** `Metric.from_context("rmsle", target_transform="log")`, with the immoscout-style reason.
  - This keeps the data, the target and the split.
  - LightGBM still ranks above the ridge regression under RMSLE (claim auditor).
  - The domain practitioner calls RMSE in dollars defensible, so if the curator keeps it, it is a MET-10 weighing call with a recorded exception. I recommend the switch.

**6. The cleaning problems are real and small. Fix each in the definition.** (P7 · CLEAN-1, CLEAN-11 Should)
- **$9,999 prices.** I concede.
  - The placeholder regex removes 443 real charm prices. Their year and mileage match the $9,995 and $10,000 trucks, so this drops rows by the target's own value.
  - The regex also drops 8,888, 7,777 and 6,666 prices.
  - Fix: allow only 5+ repeated digits plus 1234, 12345 and 123456.
- **Same truck on several sites in one scrape.** The comment and the code disagree.
  - Size: 7.2% of the rows with a non-round mileage; 12.7% of the May 2021 window.
  - It never crosses the split (same scrape), so it is not a leak. Dropping the copies changes the RMSE by at most 1.6%.
  - Fix: take `region` out of the second dedup key when the mileage is present, following `fiat_500`'s one-row-per-car decision. Or keep the key and correct the comment. Either way the comment must match the code.
- **Placeholder and impossible values.** Set them missing with one rule each and keep the rows, as in churn_telco and gallstone:
  - mileages under 100 on trucks at least 2 years old: 547 rows;
  - impossible values for an F-150: `fwd` (2,465 rows), cylinders other than 6 or 8 (219), coordinates outside the US (~53).
- **Numbers and wording:**
  - the Canadian row count is 437, not 483;
  - the anomaly line should say the drop in missing mileage is Craigslist's form change around 30 Nov 2020, which a deployed model would meet too.
- **Why the dataset stays:** none of these changes what the target means. Together they touch under 4% of rows. A quality problem is "fixed when the fix is cheap and safe"; it never excludes the dataset.

**7. The dropped seller type and title would make the task better, but leaving them out is not a reason against shipping.** (USE-6 Must · CLEAN-19 Should · P1)
- USE-6 makes an input known at the prediction point *legitimate*. It does not require us to ship every such input. Without them the task is valid, just harder.
- **Seller type (owner or dealer, from `/cto/` or `/ctd/` in the url):** cheap and safe, holds no personal data, and every actor sees it. Its own gain is small (−0.2% to −0.7% RMSE). Add it.
- **The title slug:** worth −7% to −11% RMSE together with the seller type. But the definition never read the title text for privacy reasons, and the practitioner checked slugs for phone numbers only.
  - P1 ranks above P6. Shipping the slug is the curator's call after a check for names and addresses, with slug-derived trim and cab flags as the milder option.
  - The decoded VIN codes are optional in the same way (column auditor).

**Summary for the record:**
- **Validity:** USE-5 holds (fit approximate, `fit_reason` to reword). SPLIT-14 holds. LEAK-42 verdict 3, relistings kept with a note, measured ≤1.9%.
- **Value:** TP holds. MET-11 is a departure, fixed by switching to `rmsle` from context.
- **Quality:** the CLEAN-1 and CLEAN-11 items above, fixed in the definition.
- **For the curator:**
  - whether to ship the title slug (after a P1 check);
  - whether to drop copies across sites within a scrape, or keep them and correct the comment.

**Advocate rebuttal: `craigslist_used_vehicles_f150`**

The critic and I agree on what matters: the dataset ships, the task is real, the split and its five windows stand, and the relisted trucks stay under LEAK-42 verdict 3. What is left is which definition fixes come first. I concede five points and part of the sixth.

**1. One truck on several sites: conceded. I drop my either/or.**
- I offered "drop the copies, or keep them and correct the comment". The critic is right that only the first option meets the rule.
- LEAK-42 is a Must. Verdict 2 names "copies of one record (… listed again …)" and says they "go down to one row per unit". A dealer posting the same truck on several sites in one scrape is exactly that case.
- A comment saying "one row per truck and site" would describe the problem without fixing it.
- **Fix:** drop `region` from the second dedup key, `["scrape_date", "year", "odometer", "price", "region"]` at `dataset.py` as reviewed (line 216), for rows with a non-round mileage. This keeps one row per car, as `fiat_500` does.
- **What follows:** under LEAK-42's last paragraph, every drop is a point for the curator to discuss. The issue must give:
  - the share of rows dropped (7.2% of the rows with a non-round mileage, 12.7% of the May 2021 window);
  - the price distribution before and after the drop.

  The RMSE moves by at most 1.6%, so I don't expect the target's meaning to change.

**2. Seller type and title slug: seller conceded in full, slug disputed only on order.**
- **Seller:** I concede. CLEAN-3 says an identifier that carries meaning is processed into that meaning, and the url's `/cto/` or `/ctd/` section is that meaning. USE-6's reason ("dropping it changes the task") applies, since every actor sees who is selling. Ship `seller` as a categorical. It carries no P1 risk.
- **Slug:** USE-6 makes the slug a legitimate input. It does not settle privacy, and P1 ranks above P3 and P6.
  - The definition deliberately never reads the title (`dataset.py` as reviewed (line 39-41)), because 70-80% of the posting texts hold a phone number.
  - The slug is a shortened copy of that title. Only phone numbers have been checked in it, not names.
  - So the slug ships after the names and addresses check, not before. If the check is clean, I agree USE-6 then argues for shipping it, since it is the input that holds the trim (the −6.8% to −10.4% RMSE gain).
- This is the same remedy the critic proposes, so nothing is actually in dispute. I only want it on record that the order is P1 first, then USE-6.

**3. The $9,999 regex: conceded.** Both briefs propose the same fix (CLEAN-11): drop `9999` from `PLACEHOLDER_PRICE` and match only 5 or more repeated digits, plus 1234, 12345 and 123456.

**4. The metric: conceded.** Both briefs propose `Metric.from_context("rmsle", target_transform="log")` with the immoscout-style reason (MET-11, precedent F1).

**5. Impossible values and placeholder mileages: conceded.** Both briefs give the same counts and the same remedy: set each to missing with one rule and keep the rows (CLEAN-10, CLEAN-11; churn_telco and gallstone).

**6. Notes the data refutes: conceded, with one addition.**
- I accept every item: the COVID wording, the unseen 3-16 weeks before each window, 437 Canadian rows rather than 483, and `fit_reason` naming the relistings as a leak kept on purpose with the per-window shares.
- **New point I accept:** the Mar 2020 window trains on 42.9% of the rows without version 1. SPLIT-14's 50% floor therefore rests on version 1. Builder issue 2 must say so.
- **Why that leaves the split as it is:** version 1 belongs in training on its measured order. Listing ids follow posting dates (r = 0.99998), and no listing of version 2 comes before the bulk of version 1. Only its calendar date is inferred, and the split never uses that date.
  - This is a wording fix (EV-1). Version 1 can be tagged `Time: Inferred` if the curator wants (precedent F3).
  - It is not a reason to drop that window.

**What reaches the curator**
- **No disagreement is left between the two sides.** Fixes 1-5 go into `dataset.py` in one pass, and fix 6 into the notes and the issue text.
- **The curator decides two things:**
  - whether the slug passes the P1 check for names and addresses;
  - whether the share and distribution of the cross-site drop are acceptable, as every drop must be under LEAK-42.

</details>

<details><summary>Critic</summary>

**Opening brief (critic): craigslist_used_vehicles_f150**

I'm not asking to exclude the dataset. The task is real, the split is right and no Must breaks beyond repair. It should ship only after the changes below. Points run validity first, then value, then quality.

**1. One truck posted on several sites counts several times (P5; LEAK-42, Must; the notes do not match the code)**
- **Problem:** The second dedup key includes `region`, so a dealer's truck posted on N sites stays as N rows. The notes and `task_summary.row` say "one row per truck".
- **Effect on the task:**
  - A test window scores the same truck many times.
  - Training over-weights dealers who post widely.
  - The worst case is the newest window, the one a deployed model meets.
- **Evidence:**
  - 4,431 of 61,515 rows with a non-round mileage (7.2%) repeat year, exact mileage, price and model string on another site of the same scrape (claim auditor, claim 4).
  - In May 2021 there are 1,681 extra rows, 12.7% of the window. One truck (83,066 miles) appears 39 times (column auditor, finding 1).
  - None of these copies crosses the split, so this is not a leak.
- **Rule:** LEAK-42 (Must), verdict 2: copies "listed again" go down to one row per unit.
- **Precedent:** fiat_500 keeps one row per car whatever the place (Lennart, 2026-10-14; precedent checker F2).
- **Remedy (fix the definition):** for rows with a non-round mileage, drop `region` from the second key. The fallback, if the curator rejects that, is a note that says "one row per truck and site", but that leaves the double scoring in place.

**2. Two inputs every advert shows are dropped: owner or dealer, and the advert title (P3; USE-6, Must; CLEAN-3)**
- **Problem:** The url was dropped as an identifier. It also holds the seller section (`/cto/` owner, `/ctd/` dealer) and the title slug.
- **Effect on the task:** Without them the model prices a truck while hiding the advert's headline and who is selling. Both are things the seller, the buyer and the marketplace all see.
- **Evidence (domain practitioner):**
  - Every row has `cto` or `ctd`. Dealers list comparable trucks $500–2,200 higher in every scrape.
  - 99.9% of rows have a title slug. In 51% of the rows with a bare "f-150" model string, the slug names the trim.
  - Adding the slug flags plus seller type cuts RMSE by 6.8–10.4% in all five windows.
  - The largest May 2021 errors are premium trims listed as a bare "f-150".
- **Rule:**
  - USE-6 (Must): anything known at the prediction point is a legitimate input; dropping it changes the task.
  - CLEAN-3: an identifier that carries meaning is processed into that meaning, not dropped.
- **Remedy (fix the definition):**
  - Ship `seller` (owner / dealer) as a categorical. It carries no privacy risk.
  - Ship the slug with the city prefix stripped, as a second `string` feature. Before that, scan it for phone numbers and personal names (P1). The practitioner found no phone numbers, but nobody checked for names. If the curator is not satisfied on P1, the slug stays out with a note and `seller` ships alone.

**3. Real asking prices are dropped because of their value (P4/P7; CLEAN-11, Should: a row leaves only when it is no task row or a copy)**
- **Problem:** `PLACEHOLDER_PRICE` matches `9999` and any digit repeated four times.
- **Evidence (claim auditor, claim 3):**
  - The regex removes 530 rows. 443 of them are trucks at $9,999.
  - $9,999 is a charm price, not a placeholder: median model year 2008 and about 148k miles, the same as trucks at $9,995 and $10,000.
  - Its count (443) fits the neighbouring charm prices ($8,999: 357; $10,999: 361).
  - Real prices of $8,888, $7,777 and $6,666 go too.
- **Effect:** A hole in the target distribution, cut by the target's own value.
- **Remedy (fix the definition):** remove `9999` from the regex, and limit repeated digits to five or more (11111, 99999) plus 1234, 12345 and 123456.

**4. The metric is the fallback where the context names one (P6; MET-11, Must for the origin; MET-3)**
- **Problem:** The definition declares `fallback` RMSE in dollars. MET-11's own example of a `context` metric is a price: "a price's error matters relative to the price, so `rmsle`."
- **Evidence:**
  - Prices run from $1,000 to $150,000.
  - The dearest 10% of trucks carry 36–52% of the squared dollar error in every window (claim auditor).
  - Every other price task with a log target uses `rmsle` from context, including immoscout, also a scraped asking price. The precedent checker (F1) found no fact that sets this dataset apart.
  - The definition records no reason for the departure.
- **Remedy (fix the definition):** `Metric.from_context("rmsle", target_transform="log")`, with the immoscout-style reason. If the curator keeps RMSE, it is an exception that needs a stated fact.

**5. Impossible values and placeholder mileages kept (P7; CLEAN-10, CLEAN-11, Should)**
- **Evidence (column auditor findings 3–4, claim auditor claim 14):**
  - 547 rows read under 100 miles on trucks at least two years old. Their median price is $12,900 against $16,495 for the rest, so they are not near-new trucks.
  - `drive = fwd` on 2,465 rows, though no F-150 is front-wheel drive.
  - 219 cylinder counts other than 6 or 8.
  - About 53 coordinates outside the US.
- **Remedy (cheap and safe):** set these values to missing and keep the rows, one rule each, with counts in the notes. This is a quality point and no reason to hold the task back.

**6. The notes state things the data refutes (EV-1, EV-2; writing)**
- "Mar 2020 … the start of COVID-19" is wrong.
  - The scrapes are dated by upload, and the listings of versions 2–6 are 5–10 weeks older than their upload dates.
  - The Mar 2020 window has 50 COVID mentions in 539,759 adverts (0.01%). The pandemic's start falls in the Jun 2020 window (claim auditor 5, split auditor 1).
- "No gap" is right for the label, but the notes do not say that the scrape schedule leaves 3–16 weeks unobserved before each test window (split auditor 2).
- The Mar 2020 window clears SPLIT-14's 50% floor only because version 1 is in training. Without it the window trains on 42.9%. Version 1's date is inferred, though its order is measured. Builder issue 2 must say this (precedent checker F3).
- The notes count 483 Canadian F-150 rows; the data has 437.
- `fit_reason` lists the relisted trucks as a gap in the fit. They are a leak kept on purpose (USE-8).
  - The record should state LEAK-42 verdict 3: no listing id appears in two periods, so every cross-scrape copy is a new posting, a repost the use case sees.
  - It should also give the same-truck-same-price share: 4.4% of the Mar 2020 window and 8.2% of Jun 2020.
- **Remedy:** reword `splits_comment`, the `SCRAPE_DATES` comment, `fit_reason` and the issue text. No re-split.

**What I am not arguing:**
- **Relisted trucks across the split:** keeping them follows LEAK-42 verdict 3 and the house_sales and melbourne precedents. Dropping them moves the error by only −1.6% to +1.9%.
- **Leaving out the 2026 scrape:** fine.
- **The temporal leaf and its five windows:** fine.
- **The model string shipped as text:** fine.

Verdict: ship after changes 1–4. Changes 5–6 are cheap and should come in the same pass.

The advocate agrees on most points, so what's left to dispute is narrow.

**Critic rebuttal: craigslist_used_vehicles_f150**

The advocate and I now agree on the verdict: ship after changes to the definition, not exclusion. We still disagree on two points and one number.

**1. The task is real and it replaces fiat_500. Concede.** USE-1, USE-5 and TP-6 hold. I never argued otherwise.

**2. The split. Concede.**
- The split matches the application, and the wording fixes the advocate accepts are the ones I asked for (EV-1).
- I accept tagging version 1 as `Time: Inferred`, as was done for diabetes_130_us. Builder issue 2 must still say that Mar 2020 trains on only 42.9% without version 1, which is below SPLIT-14's floor (precedent checker F3). The advocate doesn't dispute this.

**3. Relisted trucks kept under a temporal split. Concede.** This is LEAK-42 verdict 3. It was already on my list of points I'm not arguing. The `fit_reason` rewording we both ask for is the same change.

**4. The task is worth benchmarking. Concede.**

**5. Switch the metric to RMSLE. Agreed.** This is my point 4.

**6. Cleaning. I concede the $9,999 fix and the missing-value fixes. I dispute two parts.**
- **"Either way" on copies of one truck across sites.** I keep asking for the dedup, not just a note.
  - **The rule:** LEAK-42 verdict 2 (Must) says copies "listed again" go down to one row per unit. One dealer's truck posted to several sites at the same mileage and price is exactly that.
  - **Why it matters:** the copies don't cross the split, but they score one truck many times in a test window. The truck at 83,066 miles appears 39 times in May 2021, at prices within 2% (column auditor, finding 1). Copies are 12.7% of the newest window, the one a deployed model meets.
  - **Precedent:** fiat_500 keeps one row per car whatever the place (precedent checker F2).
  - **What I concede:** the score barely moves (RMSE −0.2% to +1.6%, column auditor). The key is rebuilt from the features, so LEAK-42 makes its certainty the curator's call. My recommendation stays: drop `region` from the key for rows with a non-round mileage. The note-only fallback goes on the record as a departure from verdict 2, not as an equal option.
- **"Together they touch under 4% of rows."** That is wrong. The advocate's own items add up to about 8,200 of 108,303 rows (about 7.6%, before any overlap):
  - copies across sites: 4,431
  - `fwd`: 2,465
  - placeholder prices: 530
  - mileages under 100: 547
  - cylinder counts: 219
  - coordinates outside the US: about 53

  The conclusion doesn't change: these are cheap quality fixes and no reason to exclude. But the issue text must carry the right number.
- **"Dropping the copies changes the RMSE by at most 1.6%."** That is the column auditor's figure for the copies across sites, so it is right here. A similar range, −1.6% to +1.9%, belongs to the relistings across scrapes. The record should not mix the two.

**7. Seller type and the title slug. I concede on seller type. On the slug I narrow my request but keep it.**
- **Seller type:** we agree to ship `seller` (owner or dealer) as a categorical. Its own gain is small (−0.2% to −0.7%), but every actor sees it.
- **The slug:** I dispute "USE-6 doesn't require us to ship it."
  - USE-6 gives its own reason: "dropping it changes the task." The task becomes pricing an advert without its headline.
  - CLEAN-3 (Should) says an identifier that carries meaning is processed into that meaning, not dropped. The url holds both the seller section and the title.
  - Together the slug and seller type cut RMSE by 7–11% in every window (domain practitioner). The largest May 2021 errors are premium trims listed as a bare "f-150".
- **What I concede:** P1 ranks above P6, and nobody has checked the slugs for names. So the advocate's milder option is enough: trim and cab flags built from the slug (CLEAN-19), which carry no free text, so there is no privacy risk.
- **What I ask:** ship the slug-derived flags as the default. Ship the full slug only if the curator is satisfied after the check for names. Dropping the title altogether needs a stated reason.

**Where that leaves us:**
- **Agreed:** RMSLE; the $9,999 regex fix; the impossible and placeholder values set to missing; seller type added; the wording fixes (Mar 2020, the unseen weeks before each window, `fit_reason`, the 437 Canadian rows, `Time: Inferred`).
- **For the curator:**
  - dedup across sites (my position: LEAK-42 verdict 2) or a note recorded as a departure;
  - slug-derived flags (my position) or no title input.

</details>
