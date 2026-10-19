# account_debt_south_africa

**Outcome:** added. 101,871 accounts of eight South African municipalities from the uploader's Kaggle file; binary
target bad debt at the extract, IID (`ForcedIIDFromTemporal`). The three columns that set the label, the payment
totals of the label window and seven runs of the file without recorded debt are dropped. The AI recommends shipping
it; the run drop is the main open call.

**Main points:** Seven runs of the file (20% of rows) hold no recorded debt and are dropped by a rule on the file
order: keep, drop or retire? The three label-rule columns and the payment totals of the label window are dropped.

**Record judgment:** valid with concerns: the label is a rule of three shipped columns, 20% of the rows come from
segments of the file without recorded debt, and the payment totals sum the window at whose end the label is read
(issues 1-3).

**Issues for Lennart:**

1. **Segments without recorded debt (20% of the file): dropped by a rule on the file order. Keep that, keep the rows, or retire?**
   Seven runs of 1,185 to 8,762 consecutive rows (27,938 rows) hold no account with debt aged 90+ days or a write-off.
   Inside them 11,984 billed accounts paid nothing in two years and none is a bad debt (91.5% of the 40,984 such
   accounts elsewhere); the 2,282 that paid at most half of their billing are no bad debts either (89.6% of 6,631
   elsewhere). They are not new accounts (non-payers with 24-100 billing lines: 0% bad inside, 97-98% outside); payments
   were recorded (56.6% of the billed accounts in the runs paid something); ID numbers 0-0.7% against 53% elsewhere.
   Debt was not recorded there. Kept, they are a learnable recording artefact (membership AUC 0.988). Implemented: drop
   runs of at least 1,000 rows; the next shorter runs (334 and 218 rows) are paying accounts whose zero debt is
   consistent, and a 186-row run of non-paying accounts with ID numbers stays in (an anomaly bullet). Alternative:
   retire as `Data Quality Issue`, following ghanas_indigenous_intel ("no event" mixed with "not recorded": retire
   unless the recording process can be recovered), if a rule on the raw file order is not acceptable; or ask DMS
   Technologies which municipalities lack debt data.

2. **The label is a rule of three shipped columns.** Every account with `total90debt` > 0 or `totalwriteoff` > 0 is a
   bad debt, and all but 371 of the 74,909 others are not (138,138 of 138,509 rows); AUC 0.999 with them. Dropped, as
   the uploader's notebook does ("These fields are used to determine whether a consumer is already a bad debt and not to
   predict whether they will become a bad debt"). OpenML 43838 ships them as features, so a benchmark that uses that
   copy unchanged scores a lookup (the record lists the dataset in TabSTAR; its preprocessing was not checked). No
   alternative proposed.

3. **The payment totals are dropped (prediction point).** `totalreceipting`, `avgreceipting` and `collectionratio` sum
   the payments of the two years at whose end the status is read; arrears are billing less payments plus the opening
   balance. The bad-debt rate falls from 91.5% for accounts that paid nothing (97% when billed over 24-100 lines) to
   14.7% for those that paid 87.5-105% of their billing. Dropped by the mutual_funds_india rule (patterns §D.2).
   Implemented: dropped (AUC 0.874). Alternatives: keep them as the uploader does, whose notebook's main feature is the
   collection ratio (AUC 0.952); or keep only the static profile, category, property value and size and `HasIDNo`
   (0.832). A deployed model with them mostly flags accounts the municipality's age analysis already lists.

6. **The uploader's cohort filter.** 8,700 accounts dropped: 903 not billed in the window, 7,722 with a net credit, 121
   with negative payment totals (46 overlap); 77.8% are bad debts whose debt predates the window. Implemented as the
   notebook does. Alternative: keep them.

7. **Duplicates kept.** 6,355 exact duplicate rows (6.2%, groups up to 162); 8.1% of the test rows of split 0/0 have an
   exact copy in train, and ROC AUC there is 0.874 on all test rows, 0.867 without them. Implemented: kept, warning
   accepted. Alternative: drop exact copies (wine_quality precedent), which would remove plausible distinct accounts.
