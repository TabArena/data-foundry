# mobile_churn

**Outcome:** added. Prepaid accounts of one unnamed operator (June to August 2013), churn after the record month,
binary, IID over accounts; the 12,262 SIM cards never activated are dropped. Ship if the unknown source is accepted
(issue 1).

**Main points:** Never-activated SIM cards are dropped in every month (12,262 rows). The source and the churn definition
are unknown.

**Record judgment:** valid with concerns. The curator accepted the missing source ("data looking very good and
real"); the counter-argument is issue 1. Churners and stayers share their month's snapshot date (not the
churn_telco_europa pattern), the features do not end at the churn as far as the data show, and the rows copy no
other churn file.

**Issues for Lennart:**

1. **Keep a dataset whose source and churn definition are unknown?**
   - Evidence:
     - No description on Kaggle, licence "unknown".
     - The one discussion thread (2021-12-27) asks "can you give me the time frame of the collected data, and its
       provenance" and has no answer.
     - OpenML 44231: "No description available", creator "UNK".
     - A GitHub code search for the column name finds only later users: the TabSTAR curation file, a Teknasyon hiring
       case, a CTGAN-ENN paper repository.
     - The churn definition and its horizon are undocumented. The data place the label after the snapshot for both
       classes, but cannot show its window.
   - Clues for a search (the verifier's, rechecked):
     - activations start on 2008-01-22, with 2,929 accounts that day and 1,725 the next: a system or operator start;
     - about 92 days of activity history;
     - on-net calls are rare: 0.3 per account and month, against 16.3 off-net and 1.5 abroad. That suggests a small
       operator or an MVNO;
     - placeholder dates 2010-01-01 and 2012-09-28;
     - prepaid, June-August 2013.
   - Implemented: added, following the curator's acceptance.
   - Alternative: No with `Missing source information`, as the guidelines' decision pattern says.
   - Caveat: the WebSearch budget of my session, and of the verifier's, was used up. A Google search for
     `"user_no_outgoing_activity_in_days"` or `"mobile-churn-data.xlsx"` might still find an origin.

2. **Accounts never activated are dropped in every month, June included. Accept, or one of the alternatives?**
   - Implemented: rows with `user_intake` = 0 and no activation date are dropped: 12,262 rows (4,982 June, 35 July,
     7,245 August) with churn 69.4%, holding 8,515 of the 13,907 churners. Kept: 54,207 rows, churn 9.9%. LightGBM
     3 x 3: 0.848.
   - Alternative A, the verifier's and coordinator's rule (after June only): 59,189 rows, churn 13.7%, 0.870. It
     keeps 4,982 June SIMs of the same profile (churn 54.3%), 4,021 exact copies and 235 vectors with both labels.
   - Alternative C, June only (`month` dropped): 57,656 rows, 0.872. It also keeps the 4,982 June SIMs. June only
     with them dropped: 52,674 rows, 0.850.
   - Alternative D, all rows as first shipped: 66,469 rows, 0.908. A random split leaks the August batches (0.882
     with batches held together).

3. **Small column choices, all within 0.002 AUC.**
   - `month` is kept as the record month. It is constant when a deployed model scores one month; dropping it gives
     0.8479 against 0.8481.
   - `user_account_id` is dropped; TabSTAR drops it too.
   - Default-date day counts are set to missing (1970-01-01, 2010-01-01, 2012-09-28).
   - The year is 2019, the Kaggle upload and the record's year; the data are from 2013.
