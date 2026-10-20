# expresso_churn_prediction

**Outcome:** added as `expresso_churn_prediction_1m`. Churn of Expresso's customers after a three-month window,
from Zindi's full Train.csv (2,154,048 rows, shipped as the `_1m` version), IID as in the competition. REGION is
dropped as most likely filled after the window. The AI recommends shipping it.

**Main points:** REGION is dropped as most likely filled after the window; keep it as a potential leak instead?

**Record judgment:** valid with concerns: REGION is most likely filled after the observation window (issue 1), and
Zindi publishes no calendar dates.

**Issues for Lennart:**

1. **REGION is dropped as most likely filled after the window. Keep it instead?**
   - Evidence:
     - 39.4% of customers have no region. Of these, 44.8% churned, against 1.8% of customers with a region.
     - Among churners, the region is missing for 92-95% in every band of active days from 1 to 62. The share is also
       85-95% in every revenue decile and 86-96% in every tenure band.
     - Among stayers, the share falls from 67% (1 active day) to 7% (62 active days).
     - The window's own columns fall with activity in both groups. MONTANT missing: churners 93% to 13%, stayers 88% to
       1%.
     - A model of the missing region from the window's columns, fit on stayers, predicts 11% missing for the 612
       churners active on all 62 days. 94% of them have no region.
     - The region values add almost nothing among customers who have one: ROC AUC 0.913 with them against 0.912 without.
     - Cost of the drop: LightGBM ROC AUC 0.930 → 0.901 on 400k rows; in the leak probe, 0.928 → 0.899.
   - Implemented: dropped. The precedent is mic's outcome-driven missingness. REGION is not an anonymised host field
     like kick's or homesite's.
   - Alternative: keep it as "Potential leak, kept on purpose", described as probably post-outcome. What would settle it
     is how Expresso fills REGION.

4. **FYI: the extract order.**
   - The 3rd-place solution decoded user_id ("an SHA-1 hash of an integer", Zindi discussion 9379) and used it as a
     feature.
   - Churn varies along the decoded order: 13-23% per block of 100k rows.
   - The file is one snapshot, and Zindi's test set is random within it.
   - Implemented: IID, with user_id dropped (the neighbours' churn in that order gives ROC AUC 0.55).

5. **Minor.**
   - `ARPU_SEGMENT` equals round(REVENUE / 3) in all rows. Kept as released; the alternative is to drop it as a copy.
   - `year = "2020"` is the first release (UmojaHack), while the BibTeX cites the 2021 competition. This is the same
     year-semantics question as pkdd.
