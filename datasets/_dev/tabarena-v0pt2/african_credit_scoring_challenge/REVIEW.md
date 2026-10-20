# african_credit_scoring_challenge

**Outcome:** added. Zindi's African Credit Scoring Challenge (Kenyan lender data, 58,953 rows): binary target
default at disbursement, nine temporal windows of at most 30 days, with three leaks removed (the repay amounts, the
lender rows labelled 0 by construction, the unsettled labels). The AI recommends including it, with concerns: the
window scheme, the near-chance 2024 windows and the customer history are open.

**Main points:** The window scheme. Three leaks removed: the repay amounts, the zero-share lender rows and the
unsettled labels. Most of the signal is the customer's history.

**Record fields that disagree with the definition:**

- `required_split`: record `Grouped (NON-IID), Temporal (NON-IID)`, definition `Temporal (NON-IID)`.
- `tag`: record `Non-IID (Grouped)`, definition `Temporal (NON-IID)`.

**Issues for Lennart:**

1. **Which test windows? Bounded 30-day windows that leave the sparse 19 months (2022-12 to 2024-07) to training, or windows that also test that period with longer horizons?**
   - Implemented: Reviewer 2's variant (b) with the refit cadence made explicit:
     - 6 equal-row windows over the end of the Type_1 lending (2022-10-20 to 2022-12-01, 5-10 days each).
     - 3 x 30-day windows ending 2024-10-08.
     - Declared horizon 30 days.
     - 2022-12-02 to 2024-07-10 (1,901 rows) is training data only.
   - Alternative:
     - (a) Reviewer 2's variant: 5 Type_1 windows, three post-era windows of 6-7 months, and 2024-07-11 to 10-08 (90
       days).
     - (b) As proposed: the author's 7 Type_1 windows plus two 45-day windows.
     - (c) The author's 9 equal-row windows, whose w1 runs 573 days with 28% of its rows in products that have no
       training row.
   - Numbers: Mean ROC AUC as linear / forest / LightGBM-300 / CatBoost (seed 0) / customer-row count, then test rows
     and default rows:
     - Implemented: 0.649 / 0.632 / 0.604 / 0.675 / 0.682. Spans 5-30 days, 13,890 rows, 289 defaults.
     - (a): 0.657 / 0.647 / 0.641 / 0.665 / 0.654. Spans 6-209 days, 15,791 rows, 498 defaults.
     - (b): 0.671 / 0.645 / 0.643 / 0.708 / 0.688. Spans 3-45 days, 14,046 rows, 304 defaults.
     - (c): 0.674 / 0.648 / 0.649 / 0.704 / 0.689. Spans 3-573 days, 15,791 rows, 498 defaults.

2. **Drop the rows whose lender funds less than one unit? They are labelled 0 by construction, but dropping them selects the 2022 test windows on a field recorded after disbursement.**
   - Implemented: Dropped all 8,899 rows with Amount_Funded_By_Lender < 0.5. That is the author's 8,520 zero-share
     rows plus 379 tiny-share rows, 56 of which fall in test windows. 1,978 zero-share rows fall on test-window dates.
     The 2022 windows lose 8.2-17.9% of the rows of their dates.
   - Alternative:
     - Keep them with the share columns, as v1 did: a model learns that a lender amount below one unit means repaid.
     - Keep them and drop both share columns: about 90-130 defaults stay labelled 0.
     - Drop only the zero-share rows (the author's filter).
   - Numbers:
     - 0 of 8,899 rows are labelled 1.
     - Same customers and months: 1.04% of the dropped loans carry a charge over 20%, against 0.40% of their other
       loans. Customers borrowed again after 1.1% of the charged dropped loans, against 87-88% after uncharged loans.
     - Untuned LightGBM: 0.639 implemented, 0.646 with all rows kept, 0.656 dropping only zero shares.

3. **How long until a label counts as known?**
   - Implemented: 30 days after the due date. 802 rows (84 labelled 1) are dropped, and training sides hold rows with
     due_date + 30 < window start.
   - Alternative: Due date only, or all earlier loans (v1 used a 3-day gap).
   - Numbers:
     - Untuned LightGBM: 0.639 with the 30-day rule, 0.676 with due date only, 0.685 with all earlier loans.
     - Default rate of 2024 rows: 19.6% / 15.3% / 11.6% at 1-7 / 8-14 / 15-30 days past due, against 6.9-10.2% from
       31 days on.

4. **Keep customer_id and keep the dataset, given that most of its signal is the customer's history and the three 2024 windows are near chance?**
   - Implemented: customer_id kept as a categorical, and the dataset kept under task_probes.md rules 2 and 4.
     Re-check against the first tuned runs.
   - Alternative: Drop customer_id, so every loan is scored like a new applicant. Or hold the task-worth decision
     until tuned results exist.
   - Numbers:
     - LightGBM: 0.639 with customer_id, 0.527 without. CatBoost (3 seeds): 0.672 with, 0.606 without.
     - The count of the customer's training rows alone scores 0.682: 0.516-0.621 on the 2024 windows, 0.616-0.800 on
       the 2022 windows. It is at or above CatBoost in 6 of 9 windows.
     - 2024 windows: linear 0.535-0.631, CatBoost 0.484-0.619.
     - Test rows of a customer with a training row: 85-96% in 2022, 12-44% in 2024.

5. **Release note (not a verdict reason): may the collection redistribute a file that reached Kaggle through a participant's upload made after the close?**
   - Implemented: License attribute 'Zindi Competition Rules'. download_description and the licence bullet say the
     copy is a participant's upload after the close.
   - Alternative: Ask Zindi or the host before release.
   - Numbers:
     - Zindi rules: 'The data is private property of the client.'; participants must notify Zindi 'upon learning of
       any unauthorised transmission of or unauthorised access to the challenge data'.
     - The Kaggle copy was uploaded 2025-01-14 15:51 by thelastsmilodon (32nd place), with licence 'other' and an
       empty description.
