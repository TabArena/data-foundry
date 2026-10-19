# credit_card_customers

**Outcome:** added; recommended `No` (`AHDS`, `Missing source information`). BankChurners.csv, LEAPS teaching case 11
via Kaggle, as an IID binary task: will a credit card customer close the account? The AI recommends `No` because the
activity columns look constructed (issue 1); the curator accepted the unknown source, so the folder stays until he
decides.

**Main points:** Looks constructed: the 12-month count is Q1 + Q4 in every row; months inactive are unrelated to it.

**Record judgment:** valid with concerns: the columns look constructed (issue 1), the 12-month window may end at the
account closure (issue 2), and the source is a teaching case whose material is gone (issue 3).

**Issues for Lennart:**

1. **The data looks constructed. I recommend `No` + `AHDS` + `Missing source information` (Lennart's call).**
   - Verifier finding 1, which I accept after re-running its key numbers with my own code:
     - **Count identity.** The 12-month count equals the Q4 count plus the Q1 count. Total_Ct_Chng_Q4_Q1, their ratio to
       3 decimals, splits Total_Trans_Ct into two whole counts in all 10,127 rows. One of them is a rounding tie (51/80
       = 0.6375 given as 0.638); the verifier counts 10,126.
       - Controls: shuffled totals give 523-592 rows (verifier: 587). Home Credit's real card statements give 9 of 8,920
         (reproduced).
       - Q1 and Q4 cannot both be quarters, since that leaves no Q2 or Q3 transactions for anyone. Read as halves, the 7
         customers without a second-half transaction would have at least 6 inactive months; they have 2-4.
       - On its own, the identity would fit a half-year reading. The proof is the joint picture: the identity plus the
         independences below.
     - **Inactivity.** Months_Inactive_12_mon is unrelated to the count: Spearman −0.051, within class 0.012 and 0.025.
       Home Credit gives −0.601 (reproduced).
     - **Spend vs limit.** The 12-month amount is unrelated to the credit limit: Spearman 0.028. Home Credit gives 0.447
       (reproduced).
     - **Education.** A classifier tells the real rows from rows with Education_Level permuted within each class at AUC
       0.495 (verifier 0.492). The same test on two real credit tables gives 0.578 (Home Credit) and 0.613 (Taiwan); the
       verifier has 0.587 and 0.621. Months inactive: 0.530 (0.527).
   - My earlier marks, from the raw file (2026-10-07):
     - **Tenure is bounded by age.** Outside the 2,463 rows at 36 months, Months_on_book ≤ Customer_Age − 4 in all 7,664
       rows, and ≥ Customer_Age − 20 in 7,622. That is a parallelogram band with slope 1.006 months per year of age (r
       0.893), although tenure only spans 13-56 months for ages 26-73. The only 445 rows above the bound are under-40s
       at the filled-in 36, so the 36 was written after the tenure was derived.
     - **Gender and income.** No woman has an income above $60K: 0 of 5,358, against 3,664 of 4,769 men.
     - **Missing dependences.** Education is independent of income (Cramér's V 0.028, p = 0.23). The single share is
       flat over age: 45% at 26-35, 43% at 56-73.
     - **Clusters.** Total_Trans_Amt falls in separated clusters: 2 rows in 10,500-12,000, and 746 rows above 12,000
       with no attriter.
     - **Context.** LEAPS is a training platform, and its 2021 list calls another case's data "a dummy dataset".
   - Against: the generated-data probe finds no rule leaves, and nothing shows how the label was made.
   - Implemented:
     - the folder stays, with the extended Anomaly bullet (all numbers above) and the first decision (figure plus text);
     - `data_tags = ("2ndTierData",)`;
     - the record comment now recommends `No` + `AHDS` + `Missing source information`.
   - Alternative: retire and remove the folder, as for ecommerce_shipping, customer_satisfaction_in_airline, churn, and
     in this run stroke_prediction and hepatitis_c_egypt.

2. **Prediction point: does the 12-month window end at the account closure?** That would be the iranian_churn mechanism.
   - The source does not say. The data card has "Last 12 months" and "if the account is closed then 1 else 0".
   - Kaggle topic 203290 (2020-12-14, 3 votes, never answered) asks it: "Are the statistics of transection history for
     attired customers the history just before they cancel the cards?" It is now cited in the bullet.
   - Signs that it does:
     - all 7 customers with zero Q4 transactions, and all 54 with 6 contacts, are attrited;
     - 55% of attriters have a zero revolving balance, against 19% of existing customers;
     - the six activity columns alone reach AUC 0.980 and all 19 reach 0.994, against 0.7-0.85 for typical churn tasks
       (iranian_churn 0.986).
   - Against: most attriters still transact in Q4 (median Q4/Q1 count ratio 0.53 vs 0.72), so the window does not run
     months past the closure.
   - Implemented: kept, with a "Potential leak, kept on purpose" bullet and a revisit condition (if the LEAPS case
     material turns up).
   - Alternatives:
     - retire (the iranian_churn call needed the paper's statement, which does not exist here);
     - drop the activity block (profile + balance: AUC 0.803). That is a fix of our own invention, so I do not recommend
       it (task_probes rule 6).
   - Either way the task is near its ceiling: LightGBM log loss 0.078, and CatBoost default reaches 0.9943 with 3 of 9
     splits at or above 0.995. Tuned methods may trip `solved` and tie.

3. **Provenance is a teaching case, not a bank release.** The curator's acceptance stands, so the dataset was added.
   Counter-argument: the guidelines' "Missing source information → No" fits.
   - The trace bottoms out at LEAPS case 11, whose material is gone. No bank, country or period is named anywhere.
     Kaggle topic 215382 "Country of research" (17 votes) has no answer.
   - The paper linked in the record only uses the data, as its comment says.

4. **Minor: two filled-in or ambiguous values kept as published.**
   - Months_on_book = 36 in 2,463 rows. About 2,100 of them are filled in: the neighbours hold 317-358 rows each, and
     the 36s break the tenure-age bound. Alternative: set all 36s to NaN, losing about 340 true 36s.
   - "Unknown" kept as a category rather than NaN, following the data card and the pva precedent. Most pipelines treat
     the two alike.
