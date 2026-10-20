# 2_month_survival_rate_prediction

**Outcome:** added. SUPPORT's 8,967 patients of both phases alive after study day 3, with the phase II physiology
moved back into its rows through ICPSR 2957 (only support2's values ship). Binary target death within 2 months,
IID over patients. The AI recommends shipping it.

**Main points:** The 138 patients who died on day 3 are dropped; dnr and dnrday are dropped; no grouping by the
file's ten blocks.

**Record judgment:** valid with concerns: the source has several outcomes and four model or physician estimates
among its columns (handled); the curator's `Outdated` marker (1989-1994 care) stands.

**Issues for Lennart:**

3. **Cohort: the 138 patients who died on study day 3 are dropped.** Their day-3 values include values at death:
   heart rate 0 in 38% and mean BP 0 in 25% of them, against at most 7.1% and 3.4% of the later deaths. Alternative:
   keep them, which gives 0.822 instead of 0.814 (3 x 5-fold).

5. **dnr and dnrday are dropped** (record: "need to filter dnr"; supportdesc advises against both).
   - dnrday equals the days to discharge for all 5,842 patients without an order, and 1,659 of the 2,865 orders
     written after entry are dated after day 3.
   - Alternative: a flag for "DNR order by day 3" would be known at the prediction point (1,437 patients, 61.6% die
     within 2 months) and raises ROC AUC from 0.814 to 0.822. But the order is a care decision that carries the
     physician's prognosis.

6. **No grouping by the ten blocks of the file.** The blocks alternate phase I and phase II, probably one pair per
   hospital (undocumented). The split stays IID:
   - the use case is new patients at the same hospitals (Knaus validated on later patients of the same five);
   - five groups would make a test of shift between hospitals;
   - two phases cannot give 3 temporal windows.
