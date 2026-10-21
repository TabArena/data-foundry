# kick

**Outcome:** added. Reopened on 2026-10-21 (Lennart: "Reopen kick here") to run the test that made expresso drop
REGION on kick's `WheelType`. The test gives the same signature, so the AI now leans to dropping `WheelType` and
`WheelTypeID`; the definition is unchanged until the curator decides.

**Main points:** Keep `WheelType` under LEAK-38 as decided on 2026-10-01, or drop it under LEAK-10 as expresso dropped
REGION (issue 1). New: `PRIMEUNIT` and `AUCGUART` start to be filled mostly for good buys from October
2010, inside the last test windows (issue 2).

**Issues for Lennart:**

1. **Keep `WheelType` (LEAK-38) or drop it with `WheelTypeID` (LEAK-10), as expresso dropped REGION?**
   - Problem: `WheelType` (Alloy, Covers, Special) is missing for 24.9% of the bad buys and 1.5% of the good ones;
     70.5% of the cars without it are bad buys, against 9.7% with it. On 2026-10-01 it was kept under LEAK-38 because
     the company released it this way and the recording process is not documented. LEAK-38 speaks of anonymised
     fields, and `WheelType` is a named one, as expresso's REGION is.
   - The expresso test, run on kick (training.csv, 72,983 cars): whether the field is missing, by covariates known at
     the auction, separately for good and bad buys.
     - Good buys: missing for 1.2-1.7% in every band of vehicle age, odometer, purchase price and MMR price (quintiles).
       Bad buys: 21-39% in every band (39% for cars up to 2 years old, 21% for 7-9 years).
     - A model fit on good buys from the known covariates (age, odometer, prices, warranty cost, auction, month, make,
       buyer, ZIP, other missing flags) predicts 1.2% missing for the bad buys; 24.9% are missing. Expresso: 11%
       predicted, 94% observed.
     - In every stratum the missing flag alone separates bad buys at ROC AUC 0.57-0.77, while the missing flags of
       `Trim` and the current MMR prices stay at 0.49-0.54.
     - By auction: ADESA 47.7% of bad buys missing against 1.0% of good (flag AUC 0.734), OTHER 44.1% against 1.7%
       (0.712), MANHEIM 5.9% against 1.5% (0.522). The pattern holds in every quarter: ADESA 0.68-0.77, OTHER
       0.63-0.76, MANHEIM 0.51-0.53. A field recorded at the auction would be missing about as often for good and bad
       cars of the same auction; here the gap is 40-50 times at two of the three auction groups and appears only for
       the cars that turned out bad.
   - ROC AUC of the missing flag alone for `IsBadBuy`: 0.617 overall; 0.60-0.63 in each of the 9 shipped test
     windows; pooled within auction 0.573, within month 0.618, within auction and month 0.575, within auction and
     purchase date 0.572.
   - Effect: its whole value is the flag. LightGBM on the 9 shipped temporal windows (300 trees, mean ROC AUC):
     without `WheelType`/`WheelTypeID` 0.677, with only the missing flag 0.750, with both columns 0.750. The notes'
     0.757 and 0.691 are from the 2026-10-01 audit with other settings.
   - Against dropping: the host's test file has the same 4.5% missing (4.3% in train), so the Kaggle task had the
     flag too, and the process is still not documented. Both facts hold for expresso's REGION as well (expresso
     review panel, precedent check, 2026-10-20).
   - Implemented: kept (Lennart, 2026-10-01), with the `Potential leak, kept on purpose:` note.
   - Alternative: drop `WheelType` and `WheelTypeID` under LEAK-10 (Must; missingness that encodes the outcome), as
     expresso dropped REGION on the same test. ROC AUC 0.750 to 0.677. Other columns stay.
   - Recommendation (AI): drop. The mechanism is now measured, not suspected, which was LEAK-38's reason to keep, and
     the measured signature matches REGION's: the covariates known at the auction predict 1.2% missing for the bad
     buys and 24.9% are, a 17-fold gap that no other column's missing flag shows. Keeping it would leave two answers to the same test in the working copy.
   - Fit: `direct` either way. USE-8 was amended (Lennart, 2026-10-21): a potential leak kept on purpose, even a
     strong one like this (ROC AUC +0.066), does not make a fit approximate. Dropping two columns is not a large change
     to the task either.

2. **`PRIMEUNIT` and `AUCGUART`: filled mostly for good buys from October 2010. Test and decide?**
   - Problem: both are about 95% missing. From October 2010 they are filled more often for good buys than for bad ones
     (December 2010: 51.9% of good buys against 12.4% of bad), so their missing flag separates bad buys at ROC AUC
     0.57-0.70 in October-December 2010, which fall in the last test windows. The host's test file shows the same
     fill-in (46.0% in December 2010). This may be a second post-outcome recording effect (LEAK-10), found while
     testing issue 1 (2026-10-21); it has not been tested as issue 1 was.
   - Implemented: kept, as the definition ships them.
   - Alternative: run issue 1's conditional test on both flags; if it gives the same signature, drop both under LEAK-10
     or keep them with a note.
   - Decision needed: run the test (recommended), or keep them as they are.
