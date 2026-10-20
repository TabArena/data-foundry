# melbourne_housing_market

**Outcome:** added. A regression of the log sale price of Melbourne auction results (Melbourne_housing_FULL.csv,
January 2016 to March 2018, sales only), with the scraped realestate.com.au attributes and 9 temporal windows of
three weekly result sheets. The AI recommends shipping it; the file, the target and the scraped attributes are for
the curator.

**Main points:** Only sale prices are kept (passed-in and vendor bids dropped). The scraped attributes are kept,
checked against the auction sheets. `melbourne_housing_snapshot` is a duplicate.

**Record judgment:** valid with concerns. A scrape of Domain.com.au's weekly auction-result sheets, first published
on Kaggle, whose established use is sale-price regression. The concerns are the issues below.

**Issues for Lennart:**

1. **Which file.** Implemented: Melbourne_housing_FULL.csv (sales Jan 2016 - 17 Mar 2018, with the realestate.com.au
   attributes). Alternative: MELBOURNE_HOUSE_PRICES_LESS.csv (63,023 results to 13 Oct 2018, about 35,500 sales once
   the copies are dropped; 12 columns, no land/building attributes or coordinates; it repeats one holiday sheet on 5
   dates, 4 x 787 copy rows to drop). On the same rows and windows RMSE in log price is 0.183 with the attributes,
   0.205 without the six scraped attributes and 0.211 with the LESS columns (9 of 9 windows worse); LESS would add 7
   months and the outer suburbs before May 2017.

2. **Target is the sale price only.** PI (passed in) and VB (vendor bid) rows carry the highest or the vendor's bid
   (data
   card: "N/A - price or highest bid not available"): against LightGBM fitted on each window's training side they lie
   a median 4.3% (PI) and 6.6% (VB) below the predicted sale price, the sales 0.1% above (the verifier's run: 4.0%,
   7.0%, 0.0%); the two "unexpectedly low" prices of thread 308935 (131,000 and 145,000) are PI rows of homes that
   sold for 1,350,000 and 1,520,000. Implemented: drop PI/VB (5,939 rows with a price). Alternative: a "price or
   highest bid" target with `Method` as a feature (27,247 rows), which mixes two quantities and uses a post-auction
   field.

3. **The scraped attributes are a lookup made after the sale (the King County lesson);** keeping them is supported by
   the data. `Bedroom2` (lookup) equals the sheet's `Rooms` in 98.9-100% of the rows of each test window and 98.1-99.8%
   per quarter from Oct 2016, against 85.2% of the 3,107 sales of Apr-Sep 2016 that were looked up in April 2017. The
   dansbecker snapshot ("created in September 2017") holds the final values for its 3,290 sales of 1 Jul - 23 Sep
   2017, and the 18,396-row copy ganjedi/melbourne-housing-snapshot (same newest sale) for 5,253 of the 5,254 priced
   FULL results of those weeks: the mid-2017 lookups were made within weeks. Six 2016 sales show a construction year
   of 2017-2018 (a later building): their six scraped attributes are set to missing. Lennart's call (verifier F1):
   also blank the scraped block of the 495 sales of 2016 whose `Bedroom2` differs from `Rooms`. The verifier measured
   RMSE 0.1843 -> 0.1836 (lower in 8 of 9 windows); my re-run after the agency merge gives 0.1833 -> 0.1837 (lower in
   1 of 9), so the effect is within run-to-run noise. Implemented: keep them.

4. **Coverage changes on 27 May 2017 (closed with numbers, verifier F2).** Before, FULL holds only the inner suburbs (of
   the LESS sheets it has: all within 10 km of the CBD, 66% at 10-15 km, 2% at 15-20 km, none farther; it lacks the
   sheet of 1 April 2017); from then on every result. The same date switches the uploader's `Distance` table (140 of
   the 142 suburbs present in both periods get a new value, e.g. Airport West 13.5 -> 10.4 km) and the coordinate
   precision. All 9 test windows lie after the switch. Training only on sales from 27 May 2017: RMSE 0.1882 vs 0.1833
   (worse in 8 of 9; verifier 0.1874 vs 0.1843), outer suburbs 0.1519 vs 0.1524 (verifier 0.1517 vs 0.1521).
   Harmonising `Distance`: -0.0004 (verifier +0.0001). Implemented: keep all rows and values as recorded.

5. **Windows.** Implemented: 9 windows of 3 weekly sheets (unit="unique", horizon 3 weeks, like house_sales' 3-week
   windows), 93-1,550 test rows; the January lull (9 sales on each of 20 and 27 Jan 2018) sits in one window of 93
   sales. Both files lack the sheets of 10 Jun, 5 Aug, 2 Dec 2017 and 13 Jan 2018 (verifier), so a window can span 4
   calendar weeks; the 3-week horizon is nominal. Alternatives (decision table in the README): 4 sheets per window
   (620-1,717 rows, but 2 of 9 windows train on less than half of the rows), 4 calendar weeks (one window of 9 sales),
   calendar months (8 windows, one of 18 sales).

6. **Re-dated sheet.** The 787 FULL rows dated 6 Jan 2018 are the sheet of 16 Dec 2017: LESS holds the same 787 rows on
   16, 23, 30 Dec 2017 and 6, 8 Jan 2018. Implemented: date them 16 Dec 2017 (constant mapping, asserted count).
   Alternative: keep the file's date. The windows stay the same (the sheet lies between 9 Dec and 20 Jan either way);
   only the date of its 480 sales moves by three weeks, which matters for calendar windows.

7. **Records (verifier F7).**
   - `melbourne_housing_snapshot` (now `No`, `No Good Target (yet)`) is the same data: all 13,580 rows of
     dansbecker/melbourne-housing-snapshot match a FULL row on suburb, address, date, method, agent, rooms, type and
     price, with identical scraped values; its 18,396-row cut (Kaggle re-upload ganjedi/melbourne-housing-snapshot,
     newest sale 23 Sep 2017) has 18,395 of its rows in FULL. Proposal: the marker `Duplicate` (renamed
     `melbourne_housing_market_duplicate` by the convention).
   - Kaggle InClass competition "vitticeps" (thread 53664, visnut, 2018-04-10: "more years of data, extracted from
     pdf files ... We did not scrape the bedrooms etc data, ours are simulated") is a second extraction of the same
     Domain sheets with simulated attributes. It has no record; if it is ever proposed, it is out (simulated
     attributes) and overlaps this dataset.

8. **Repeated reports.** Same address within 60 days: same price = one sale reported again (36 rows, 0-35 days apart,
   first report kept); different price = conflicting (3 addresses, 4-35 days apart, both reports dropped). Nine of
   the 45 kept resales are 63-126 days apart, eight within 11% of the first price, possibly corrected re-reports.
   Alternative: treat repeats within 6 months by the same agent as one sale.

9. **Year (verifier F6, Lennart's call).** Implemented `year = "2018"`: the Kaggle dataset's last update (2018-10-14)
   and
   the version used. The dataset was public by 27 March 2017 (thread 30748, the first forum post), and house_sales
   uses the year of first distribution; with that convention it is "2017".

10. Licence: CC BY-NC-SA 4.0 (Kaggle page), noted; the data are scraped from Domain.com.au and realestate.com.au
    (an unanswered forum question asks whether Domain allows it, thread 53664).
