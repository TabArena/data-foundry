---
unique_name: taiwanese_bankruptcy_prediction
name: company_bankruptcy_prediction / taiwanese_bankruptcy_prediction
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2020'
required_split:
- Random (IID)
source_links:
- https://doi.org/10.24432/C5004D
notebook_path: datasets/beyond_iid/old_iid/taiwanese_bankruptcy_prediction/taiwanese_bankruptcy_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/taiwanese_bankruptcy_prediction/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

The data were collected from the Taiwan Economic Journal for the years 1999 to 2009. Company bankruptcy was defined based on the business regulations of the Taiwan Stock Exchange. Might be a duplicate as I remember a similar dataset

Could require temporal split. paper does not clearly state at which points in time the features vs. the target were collected. Maybe features are from three years before bankruptcy

Most features seems to be time invariant

Potential issue: temporal

Lennart: Not time-based features, thus could be usable

Andrej: Need to verify correct lag between features and target

CC (2026-10-19, Lennart): 67 numeric columns are min-max scaled over all companies; kept, with a `Potential leak, kept on purpose` note in the definition: a scaling over all rows is no strong leak and often happens in reality. It is a reason for `No` only when a strong leak is suspected or the data can be rebuilt.

## Reference

Liang, D., Lu, C.-C., Tsai, C.-F., and Shih, G.-A. (2016) Financial Ratios and Corporate Governance Indicators in Bankruptcy Prediction: A Comprehensive Study. European Journal of Operational Research, vol. 252, no. 2, pp. 561-572
