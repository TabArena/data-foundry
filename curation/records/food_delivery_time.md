---
unique_name: food_delivery_time
name: Food_Delivery_Time
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
- Random (IID)
original_source: Kaggle
year: '2023'
required_split:
- Temporal (NON-IID)
- Random (IID)
source_links:
- https://www.kaggle.com/datasets/rajatkumar30/food-delivery-time
notebook_path: datasets/beyond_iid/old_iid/food_delivery_time/food_delivery_time.ipynb
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Predict the time taken by the delivery person to deliver the food. Spatial. Requires special feature engineering. Might need to exclude delivery person ID. Might require temporal split; might require groups/temporal splits for delivery person ID

Potential issue: spatial data must be verifyied

Lennart: Yes, if we do some spatial feature engineering (like distance) and can ignore delivery person subgroups

Andrej: Special feature engineering necessary. Unclear whether the license is fine.

Split regime is ambiguous, so both tags are set. As shipped the dataset is IID, which contradicts the
`Non-IID (Temporal)` tag the record carried alone. The TabArena (v0.1) notebook
(`datasets/_maintenance/_old_collections/tabarena-v0pt1/food_delivery_time/food_delivery_time.ipynb`) sets
`data_tags=["IID"]`, shuffles the rows and exports the default IID splits; the BeyondArena copy under
`datasets/beyond_iid/old_iid/food_delivery_time/` is identical. The Kaggle release has no timestamp at all
(10 columns: delivery person ID/age/rating, restaurant and delivery lat/long, order type, vehicle type, and
the target), so a temporal split cannot be built from the shipped data without recovering a time index. The
only non-IID structure available is the delivery person grouping, 1320 IDs over 45,451 rows, which the
notebook records as an anomaly: using that ID as a feature may call for a cold-start (grouped or temporal)
split instead. The temporal tag reflects that open question, not the protocol the dataset actually ships with.

## Reference

https://www.kaggle.com/datasets/rajatkumar30/food-delivery-time
