# alfa_battle_2_0_task_2

**Outcome:** added. Alfa-Bank's 963,811 credit products (AlfaBattle 2.0, task 2), binary target default at issue,
513 aggregates of the client's card transactions as the top solutions built them, three two-month windows on the
issue month. The AI recommends shipping it.

**Main points:** The products of a test window's clients are dropped from each training side. Window length and gap
are open.

**Record judgment:** valid with concerns: the tabular version is an aggregation of event sequences; the time axis is
reconstructed; repeat clients are linked from the data only.

**Issues for Lennart:**

1. **Repeat clients, keep or drop?** Implemented: drop from each training side the products of the test window's
   clients (a training label not known at the prediction point; hotel_booking_demand rule). Alternative (b): keep
   them with a "Potential leak, kept on purpose" bullet: they add 0.0045 AUC for untuned LightGBM on the newest window
   (0.7774 vs 0.7729; random removal 0.7775; measured with the 127 baseline features), the competition had the same
   structure, and the ieee_fraud_detection precedent kept same-entity label history (but there a later transaction
   is labelled fraud because of an earlier reported chargeback, so the earlier label is known; here the earlier
   product's default most likely comes after the new issue). Alternative (c): a 12-month label-maturity gap, which
   also removes the general unmatured-label optimism, leaves 13.5-26.7% of the rows for training (below the 50%
   floor).

3. **Window length and gap.** Implemented: 3 windows of 2 months, no gap (oldest train side 581,221 rows, 60% after
   the filter). Alternatives: `gap=1` like the competition's unreleased month, or 3 one-month windows (months 21-23).
