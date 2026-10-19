---
unique_name: online_retail
name: online_retail
checked_by:
- Andrej
suggestion: TBD -> Yes
decision_markers:
- No Good Target (yet)
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: UCI
year: '2012'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: TBD
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/352/online+retail
- https://doi.org/10.24432/C5BW33
- https://www.kaggle.com/datasets/shahnawaj9/online-retail
source_row: 612
type_adapter_id: curation-record-v1
---

## Comments

transactions occurring between 01/12/2010 and 09/12/2011 for a UK-based and registered non-store online retail. Same uploader as for "Online_Retail_II" dataset. Could try to predict cancellations, but unclear whether that makes sense

**AI note (two-regime-zero audit, 2026-10-19):** the two-regime-zero workbook
(`curation/inputs/two_regime_zero_datasets_v4.xlsx`, Master row 53, "UCI retail-item demand benchmark", 4,070 item
series) is this dataset. Turkmen et al. (2021, PLOS ONE 16:e0259764, Sec. 5.2) build their "UCI" intermittent-demand
series from "demand records of retail items of 4070 individual items between 01/12/2010 and 09/12/2011", citing UCI
and Chen et al. (2012). A fresh download on 2026-10-19 has 541,909 transactions and 4,070 StockCodes, as stated. The
paper keeps 1,381 daily item series of the last three months (77-86% zero days in a rebuild; 69 of the 374 calendar
days have no invoice at all, 53 of them Saturdays). Daily item demand is a forecasting target and does not give this
record the tabular target it is waiting for, so no new record was made.

## Reference

Data mining for the online retail industry: A case study of RFM model-based customer segmentation using data mining
By Daqing Chen, Sai Laing Sain, Kun Guo. 2012

Published in Journal of Database Marketing and Customer Strategy Management, Vol. 19, No. 3
