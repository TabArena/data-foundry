---
unique_name: ecommerce_shipping
name: E-CommereShippingData / ecommerce_shipping
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: No (Retired)
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Missing source information
original_source: Kaggle
year: '2021'
required_split:
- Random (IID)
source_links:
- https://www.kaggle.com/datasets/prachi13/customer-analytics
notebook_path: datasets/beyond_iid/old_iid/ecommerce_shipping/ecommerce_shipping.ipynb
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Target is whether a product has reached a customer on time using product and customer-related features, which is strange as the delivery should not depend on the customer. But nevertheless, might be a useful task

Potential issue: questionable predictive task

Lennart: It could be a useful predictie task after removing some features, unclear otherwise

Andrej: License

CC (2026-10-01, Lennart): Leak audit deep dive (source, Kaggle tabs via the kaggle CLI 2.2.2, data):
- **Source:** the data card claims "an international e-commerce company" and says the uploader (Prachi Gopalani) made the data available from her "project on Customer Analytics stored in GitHub repository". Her GitHub account (Prachi-Gopalani13) has no such repository, the Kaggle upload is a single `Train.csv` (2021-02-23, no test file, never updated), and no earlier copy turns up on GitHub or the web; every later copy cites this Kaggle page. Her only notebook on it (prachi13/e-commerce-visualizations) is plain EDA.
- **Discussion tab** (12 threads): "where the data comes from?" (14 votes, 4 comments) and the licence question were never answered by the uploader; others ask what discount, customer rating and product importance mean, also unanswered. One thread notes that blocks A-E hold 1,833 rows each and F 3,666 ("E block is overriden").
- **The categorical columns are row-counter fill patterns.** `Warehouse_block` is a function of `ID mod 6` (cycle D, F, A, B, C, F; that is why F has twice the rows) with no exception, and `Mode_of_Shipment` a function of the position in a 137-ID cycle (22 Flight, 93 Ship, 22 Road), with 0 of 10,999 rows off the pattern. Real shipments are not assigned a warehouse or mode by their row number.
- **Two generated blocks** (from the first audit): IDs 1-3,135 are 100% late with discounts 1-65 and weights 1,001-7,846 g; IDs 3,136+ have discounts 1-10, weights mostly 4,000-6,000 g and 43.6% late; on those rows LightGBM scores AUC 0.506.
Conclusion: the file is generated, not a company export. Proposed verdict No (Retired), markers AHDS + Missing source information.

CC (2026-10-01, Lennart): **Retired (No (Retired), AHDS + Missing source information).** Main reason: two of the columns are fill patterns of the row counter, so the file is generated, not a company export. `Warehouse_block` is fully determined by `ID mod 6` (cycle D, F, A, B, C, F) and `Mode_of_Shipment` by the position in a 137-ID cycle (22 Flight, 93 Ship, 22 Road); not one of the 10,999 rows breaks either pattern. Supporting: the target is generated in two ID blocks (IDs 1-3,135 all late; after that AUC 0.506), and the source cannot be traced (the cited GitHub project does not exist; the uploader never answered the source question). Removed from the TabArena v0.2 working copy; the shipped TabArena v0.1 notebook is unchanged.

## Reference

https://www.kaggle.com/datasets/prachi13/customer-analytics
