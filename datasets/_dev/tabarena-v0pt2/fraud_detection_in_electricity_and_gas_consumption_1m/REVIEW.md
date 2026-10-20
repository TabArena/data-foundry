# fraud_detection_in_electricity_and_gas_consumption

**Outcome:** added as `fraud_detection_in_electricity_and_gas_consumption_1m`. STEG's meter-fraud finding per
client, grouped by client (one prediction per client from its invoices), with the history cut at 2013-01-01
because the later invoices carry traces of the inspections. 83,874 clients billed before and after the cut; the
invoice frame is above the row budget, so it ships as the `_1m` version. The AI recommends shipping it.

**Main points:** History cut at 2013 (inspection footprints) instead of the challenge's full history. The
per-client rule (`mean`, `any`, `last`) is open.

**Record fields that disagree with the definition:**

- `year`: record `2020`, definition `2019`.
- `tag`: record `Non-IID (Temporal)`, definition `Grouped (NON-IID)`.

**Record judgment:** valid with concerns: the invoices from 2013 carry traces of the inspections that set the
labels (issue 1; the cut removes them, but its date is read off the data), and the labels of clients who left
before 2013 look unrecorded (issue 2).

**Issues for Lennart:**

1. **History cut at 2013-01-01 (implemented) or the full history (the challenge's task)?**
   - Evidence: among the 116,360 clients billed from 2013, the fraud rate of clients whose second electricity meter
     first appears in a quarter is 7.4-11.9% for each quarter of 2012 and 23.8-25.9% for each quarter of 2013. It
     is 33.1% for all second meters from 2013, against 8.1% before.
   - Other codes show the same step. Counter status 5: 9.5% in 2012Q4, 23.7% in 2013Q1. A new `counter_code`: 7.5%
     against 35.7%. A new `tarif_type`: 7.7% against 26.1%.
   - The number of such events per quarter does not jump, so the step is in the labels.
   - 11,731 clients carry a 2013+ meter or status-5 change. 30.8% of them are frauds, against 3.8% of the others;
     they hold 47.8% of all frauds, and that flag alone scores AUC 0.70.
   - With the full history, a client-level LightGBM scores 0.848 (0.764 without the meter counts). With the cut, the
     models score 0.61-0.69.
   - Alternative: the full history of the 116,360 clients billed from 2013, with a `Potential leak, kept on purpose`
     bullet. That is the challenge's task, but about half of its frauds are recognised by the trace of their own
     inspection.
   - The cut date is read off the data. STEG or Zindi could confirm when the labels were set.

2. **Cohort: clients billed both before and after the cut.**
   - Dropped: the 19,133 clients whose last invoice is before 2013. They have 21 frauds (0.11%), and by the year of
     the last invoice the fraud rate is 0-0.15% up to 2011, 0.8% for 2012 and 3.9-8.3% from 2013, so their labels
     look unrecorded.
   - Also dropped: the 32,486 clients whose first invoice is from 2013 on (no history at the prediction date; 3.2%
     frauds).
   - Alternative (only with the full history): keep the 32,486 newer clients too, or all 135,493 as Zindi does. The
     early leavers are easy negatives: 0.869 with them against 0.848 without, client-level LightGBM.

3. **Group prediction rule: `mean` (implemented), `any` (the verifier's proposal for the cut) or `last`.**
   - On the cut, the rules tie: mean 0.685, largest 0.684, latest date 0.682-0.684.
   - The largest prediction grows with the number of invoices, and so does the fraud rate (5.3% for 1-3 invoices,
     9.4% for more than 40). Its per-client score follows the count more (Spearman 0.31 against 0.24).
   - `last` needs a tie rule: 50% of the clients have several invoices on their latest date before the cut.
   - I chose `mean`: the label belongs to the client, and every invoice is one observation of it.

4. **Context and size.**
   - The `_1m` sub-sample keeps 66,014 of the 83,874 clients.
   - With the cut, a row model averaged per client (0.685) does as well as simple client aggregates (0.662), so the
     task does not depend on the harness building group features. The context is still `all_rows`.
   - Alternative: one row per client with aggregates of our own (83,874 rows, IID). That is feature engineering the
     guidelines leave to the pipeline, and Lennart's record comment points to the invoice rows.

6. **Extract date.**
   - The data first ran on 20-22 Sep 2019. github.com/mohamedScikitLearn/AI-Hack-Individual- (created 2019-09-23)
     holds submissions for the same 58,069 test clients.
   - Yet 29,121 train invoices (17,616 clients) are dated after 22 Sep 2019, up to 2019-12-07: the dates are shifted,
     or the files were refreshed later.
   - The cut uses the data's own dates, so this changes no decision.

7. **Source and download.**
   - The Kaggle mirror is used because Zindi needs a login. A curator with a Zindi account can compare `train.zip`
     against the sha256 sums.
   - Zindi's rules forbid redistribution (noted, not a verdict reason).
