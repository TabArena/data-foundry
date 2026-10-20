# lgd

**Outcome:** added. A regression of the loss given default (`lgd`, a share from 0 to 1) of 2,545 loans of a
European bank from LTV and the loan purpose, grouped by borrower block (runs of identical LTV). The AI recommends
shipping it as a small, thin task; the problem type, the split and the meaning of `event` = 0 are for the curator.

**Main points:** A grouped regression on LGD (the record says binary and IID), with two features only. Whether
`event` = 0 is a cure is unsettled.

**Record fields that disagree with the definition:**

- `problem_type`: record `Binary Classification`, definition `Regression`.
- `required_split`: record `Random (IID)`, definition `Grouped (NON-IID)`.

**Record judgment:** valid with concerns: only two features, the record's problem type and split, and the
undocumented modifications (issues 1-5).

**Issues for Lennart:**

1. **Problem type: the record should say Regression.** The record says Binary Classification. The only binary column
   is `event`, which is 1 exactly when LGD is above the 0.00001 floor, so a binary task would predict loss vs no loss.
   The book's own task is the regression:
   - Ch. 1 p. 4: "The tenth chapter presents marginal loss given default (LGD) models and LGD models that condition
     on the selecting default event".
   - The site's ch. 10 errata (updates.html): "Page 293 - add MODEL lgd_time ~ GENERAL(ll)".
   - The R Companion code fits `lm(lgd_time ~ LTV + purpose1)` plus fractional-logit, beta, Tobit and Heckman models.
   - KU Leuven's CreditICL treats a table with the same column and bounds as an LGD regression.

   The alternative is an `lgd_clf` folder with `event` as the target. On the same splits it scores logistic ROC AUC
   0.706 ± 0.016 and log loss 0.546 against a prior of 0.599. Raw LTV alone gets AUC 0.699, so that version comes
   close to a one-feature task.

2. **Split: the record should say Grouped (NON-IID).** The record says Random (IID). Implemented now: grouped by
   borrower block (runs of identical LTV).
   - The evidence for a block being an entity:
     - LTV is equal in all 16 digits, only inside a consecutive run.
     - 70 of the 488 multi-loan runs mix the two purposes.
     - The LGD's intraclass correlation within runs is 0.50. With LTV and the file-order trend removed, the first
       two loans of a run still correlate at 0.42, against 0.02 between neighbouring runs.
     - The book defines LGD by the "default of an obligor" (ch. 1, p. 10), so a new default does not come with the
       losses of the borrower's other loans.
   - Under a random 3-fold split, 31% of the test rows would share their exact LTV with a train row (27% an exact copy
     of both features). The grouped split leaves none.
   - The gap is negligible for smooth models: spline 0.208 random vs 0.212 grouped, linear 0.192 vs 0.192.
   - Models that memorise exact LTV values gain from a random split: full-depth random forest -0.028 vs -0.138,
     extra trees -0.172 vs -0.240, 5-NN 0.074 vs 0.029, LightGBM 0.156 vs 0.146.
   - The alternative is IID as the record says.

3. **What `event` = 0 means is not settled.** No text we read says that `event` = 0 is a cure.
   - The book's R code treats event 0 as an LGD censored at 0 in its Tobit and as a mass at zero in its censored
     beta. Both support reading it as a cure (a default that ended without loss), which is what the definition says.
   - Its Heckman model treats event 0 as "not selected".
   - If chapter 10 says those loans never defaulted, the 728 rows leave the target: they would not be LGD
     observations.

4. **Only two features**, the same two the book's models use. This is the thinnest dataset in the working copy: the
   next are sepsis_survival_minimal_clinical_records (3 features) and blood_transfusion (4). Rule 4 says the task is
   not `Trivial`, but strong methods will likely tie: the book's 3-parameter fractional logit reaches 0.204, tuned
   LightGBM 0.200 and the spline 0.208. A benchmark on it mostly measures how much a method overfits a
   one-dimensional curve: default CatBoost, LightGBM and XGBoost score 0.135, 0.133 and 0.047. Keep it as a small,
   thin task, as sepsis_survival_minimal_clinical_records was kept, or drop it for lack of features: your call.

5. **"Slightly modified and anonymized"** (ch. 1, p. 14) is not explained, and the chapter-10 text was not read. Ask
   for pp. 271-313 if you have the book. It should say:
   - whether a row is a loan or a default episode, and whether one borrower's loans are listed together;
   - whether `event` = 0 is a cure or a loan that never defaulted;
   - the country and period;
   - whether LTV is taken at origination or at default;
   - whether incomplete workouts are in the data, and whether LGDs were cut at 0 and 1.

   The probes found no HMEQ-style artefacts.

6. **Row order.** The file's order carries the outcome.
   - The median LTV per 100 rows rises from 0.22 to 1.00 over rows 1-2,300, and the mean LGD follows (0.06 to 0.49).
   - The last 234 rows (from row 2,312) look like a second segment: no renting loans, median LTV 0.23, mean LGD
     0.095, against 8%, 0.71 and 0.242 before.
   - The order may be the default date within two portfolios. The file has no dates, so out-of-time validation, the
     standard for LGD models, cannot be built. The base class shuffles the rows.
   - `ForcedIIDFromTemporal` is not set: it is the tag for IID-split temporal data, and this task is grouped with no
     date evidence. The verifier agrees.


8. **Provenance lead (unverified).** KU Leuven's CreditICL (github.com/andreasgoethals/CreditICL) holds a table
   `0003.axa` (`src/data/dataset_registry.py`), flagged proprietary. Its notes (`docs/AGENTS_MEMORY.md`, 28-09-2026)
   match this file: `lgd_time` squeezed into [1e-5, 1 - 1e-5], 28.8% complete recoveries (we count 732 rows, 28.8%,
   at or below 1e-4), 5.6% total losses, and an absolute maximum of 1.98 (our maximum LTV is 1.98). So the bank may
   be the one in that slug. This is not confirmed, and no bank is named in the definition.

9. **Framework note:**
   - hidden_groups.py cannot see an entity encoded as a repeated float value (LTV here).
