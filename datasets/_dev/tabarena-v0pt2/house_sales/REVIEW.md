# house_sales

**Outcome:** added. A regression of the log sale price of King County houses sold May 2014 to April 2015, each
house rebuilt as of its sale day from the county's change log, with 9 three-week temporal windows. The AI recommends
shipping it; the rebuild and the window length are for the curator.

**Main points:** Each house's record is rebuilt as of its sale from the county's change log: a new 1.8 GB raw input
that the county updates weekly. View and waterfront stay as in the file.

**Record fields that disagree with the definition:**

- `year`: record `2016`, definition `2015`.

**Record judgment:** valid with concerns. The source file's house features were recorded after the sales; the
definition rebuilds them as of each sale. The newest month is truncated and is dropped.

**Issues for Lennart:**

1. **Post-sale record values.** The source file's house features are the assessor's record as of 18-19 July 2015.
   - Of the first changes in the 30 days after that date, 98.7% have the file's value as their old value; of the
     changes in the 30 days before it, 23.5% do.
   - For 2,151 of 20,967 rows the record changed after the sale, mostly upward, a median 112 days after it. Changes
     are 2.5-3.5 times as frequent after a sale as before it.
   - Effect, LightGBM with 3 seeds on the 9 windows: RMSE on those rows 0.156 with the file's values against 0.208
     with the record at the sale. On all rows: 0.1727 against 0.1761, worse in 8 of 9 windows.
   - Implemented: rebuild from the county's change log (option a). This adds a 1.8 GB raw download that the county
     updates weekly; the 2014-2015 events it reads do not change.
   - Alternatives: (b) drop the 1,957 rows with a rebuilt main column; (c) keep the file's values with a
     `Potential leak, kept on purpose:` bullet.

2. **Window length.** Implemented: 9 three-week windows, the convention's 3 x 3, with 659-1,565 rows each.
   Alternative: 6 calendar months (a monthly refit; 978-2,231 rows).

4. **Parts of the post-sale record left in place.**
   - `view` and `waterfront`: 154 rows had a view or waterfront attribute changed, and the file's 0-4 view index is
     not a county attribute.
   - `sqft_living15` / `sqft_lot15`: the neighbours' areas in July 2015.
   - 5 rows whose bathroom history does not add up, and 10 blank old values.

5. **Records at the sale with placeholder values.** 6 houses under construction show a living area of 8-200 sq ft at
   their sale. Kept as the record stood; the alternative is to set them to missing.

6. **May 2015 dropped** (646 rows; extract cut mid-month). Alternative: keep it as a short window.

7. **Repeated sales kept.** Alternative: the latest sale per house, as in california_house_prices_2020.
