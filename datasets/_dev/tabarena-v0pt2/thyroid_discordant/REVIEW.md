# thyroid_discordant

**Outcome:** added. The record's `Trivial` marker fails the TP-4 test run on 2026-10-21 (the best single feature
against the methods, fold by fold); the AI recommends removing the marker.

**Main points:** Remove the `Trivial` marker (issue 1).

**Issues for Lennart:**

1. **Remove the `Trivial` marker?** The marker comes from a curation comment ("It still seems trivial", after a
   simple test on another file of the collection, Hypothyroid); no TP-4 test was run. On the 30 shipped splits the
   best single raw feature, chosen on each training side, is `FTI` (free thyroxine index) on all 30, with ROC AUC
   0.822 on average (0.691 to 0.897). A default random forest reaches 0.974 (0.913 to 0.996) and LightGBM 0.973
   (0.900 to 0.996); the single feature is worse than both on 30 of 30 splits. The task probe agrees: its
   one-feature LightGBM reaches ROC AUC 0.869 against 0.976 for the random forest, and it raises no flag. Each test
   fold holds 19 or 20 discordant cases.
   - Effect on the task: none on the data; on the record the marker reads as a reason not to ship, which the numbers
     do not support. A high ROC AUC of the methods (0.97) is not the same as a trivial task; the `solved` flag needs
     0.995.
   - Implemented: nothing; the record still carries the marker. Alternative: keep it, with the reason.
   - Rule: TP-4 (Must: `Trivial` needs proof). Precedents from the same run drop the marker on the same evidence:
     differentiated_thyroid_cancer_recurrence, diabetes_3, house_prices_nominal. The curator removes markers.
   - Recommendation: remove it. Decision: remove or keep.
