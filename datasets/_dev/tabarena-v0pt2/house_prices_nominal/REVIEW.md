# house_prices_nominal

**Outcome:** added. A regression of the log sale price on De Cock's full Ames file (2,919 sales, January 2006 to
June 2010) instead of the Kaggle half the record links, with 13 two-month temporal windows. The AI recommends
shipping it; the source, the window length and the dropped outliers are for the curator.

**Main points:** De Cock's full Ames file instead of the Kaggle half. Three partial-sale outliers are dropped.

**Record judgment:** valid with concerns: the record links the Kaggle half, not the original (issue 1), and its
`Trivial` marker is not borne out (issue 3).

**Issues for Lennart:**

1. **Source: De Cock's full file instead of the Kaggle train file the record links.** Evidence: all 1,460 Kaggle
   train rows equal a De Cock row in every feature and the price; the 1,459 test rows (no prices) are the rest, minus
   the 11 sales of Greens (8), GrnHill (2) and Landmrk (1), with some values blanked; train share 47.5-52.2% per sale
   year (a random split). Implemented: De Cock's file (2,919 rows after the July 2010 cut and the 3 outliers), 13
   two-month windows of 46-191 test rows (median 98). Alternative: the Kaggle train file (1,454 rows after the July
   cut): 12 two-month windows of 22-96 rows, or 8 quarterly windows of 41-123. Record edits to consider:
   add the JSE file (https://jse.amstat.org/v19n3/decock/AmesHousing.txt) and the DOI
   (https://doi.org/10.1080/10691898.2011.11889627) to `source_links`; the folder keeps the record's name, which is
   OpenML's name for the Kaggle half, and a name such as `ames_housing` would describe the data
   (`ames_housing_dataset`, the cell-for-cell Kaggle mirror of De Cock's file, stays `Duplicate`).

2. **Window length.** Implemented two-month windows (13 windows, 46-191 test rows). Monthly windows: 26 windows of
   19-112 rows (winter months below the ~50-row rule); quarterly: 8 windows of 91-233 rows.

3. **`Trivial` marker not borne out.** `Overall Qual` alone, chosen on each training side, reaches R² 0.682 (RMSE
   0.228) against 0.901-0.904 (0.124-0.125) for the untuned linear model and LightGBM; as a per-grade mean it is worse
   than a 500-tree LightGBM (RMSE 0.119, R² 0.912) in all 13 windows; De Cock's own two-variable model (neighborhood +
   total area, p. 13 "about 80%") reaches R² 0.766 and is never better. No task-probe flag; models spread (linear - RF
   0.019 R², paired SE 0.005). Proposed: drop the marker (record comment written).

4. **Prediction point.** Implemented "a house sells" (an automated valuation model, as in house_sales and
   zillow_prize), so `Sale Type`, `Sale Condition` and `Month Sold` are known and stay, and no gap is needed (prices are
   known once a sale is recorded). Feature effects (500-tree LightGBM, 3 seeds, 13 windows): dropping `Sale Condition`
   costs +0.0047 RMSE (SE 0.0008, worse in 13 of 13), `Sale Type` +0.0000 (SE 0.0005), `Month Sold` -0.0002 (SE
   0.0007). Alternative: predict at the purchase agreement, one or two months before the sale; that needs a gap of that
   length, which changes RMSE by +0.0006 (SE 0.0010) for one month and +0.0026 (SE 0.0013) for two.

5. **De Cock's outliers.** Implemented (verifier finding 1): drop the 3 partial sales over 4,000 sq ft ($28-$40 per sq
   ft against a median of $150 for partial sales; De Cock p. 4: "true outliers (Partial Sales that likely don't
   represent actual market values)"), keep the 2 NoRidge market sales. All five sold before the oldest test window.
   Effect: the probe's linear model RMSE 0.133 -> 0.124; verifier: ridge -0.0067 (SE 0.0038), LightGBM -0.0016 (SE
   0.0013). Alternatives: keep all five (the first version), or drop all five as De Cock recommends for students
   (ridge -0.0068, LightGBM -0.0012, verifier).

6. **June 2010** has 82 sales against 97-112 in June 2006-2009, and is cheaper: mean log price 11.931 against
   11.985-12.077 in June 2006-2009 and 12.009 in May 2010 (median $149,950 against $155,000-$169,750). In the newest
   window LightGBM's RMSE is 0.202 on June and 0.089 on May, partly from two allocation sales. Late recording before
   the July 2010 extract or the market after the first-time-buyer tax credit; the file cannot tell. Kept.

7. **Allocation sales.** The 24 "Alloca" sales (two linked properties with separate deeds; 16 of them in blocks of
   neighbouring parcels sold in one month, e.g. 8 SawyerW duplexes in June 2009 at $113,722-$153,337) and 12 "AdjLand"
   purchases are kept with the sale condition as a feature; a block shares a window. Their price can be a share of a
   joint price: in the newest window two IDOTRR allocation sales ($50,138, $55,993; residuals -0.55 and -0.56) raise
   LightGBM's RMSE from 0.145 to 0.157. Alternative: drop the 24 Alloca rows.

8. **Licence (note only):** JSE's policy asks for the author's consent to use the data in published material
   (https://jse.amstat.org/jse_users.htm).
