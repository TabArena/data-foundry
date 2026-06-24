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
year: '2016'
required_split:
- Random (IID)
- Temporal (NON-IID)
source_links:
- https://doi.org/10.24432/C5004D
type_adapter_id: curation-record-v1
---

# company_bankruptcy_prediction / taiwanese_bankruptcy_prediction

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

The data were collected from the Taiwan Economic Journal for the years 1999 to 2009. Company bankruptcy was defined based on the business regulations of the Taiwan Stock Exchange. Might be a duplicate as I remember a similar dataset

Could require temporal split. paper does not clearly state at which points in time the features vs. the target were collected. Maybe features are from three years before bankruptcy

Most features seems to be time invariant

Potential issue: temporal

Lennart: Not time-based features, thus could be usable

Andrej: Need to verify correct lag between features and target

## Reference

Liang, D., Lu, C.-C., Tsai, C.-F., and Shih, G.-A. (2016) Financial Ratios and Corporate Governance Indicators in Bankruptcy Prediction: A Comprehensive Study. European Journal of Operational Research, vol. 252, no. 2, pp. 561-572
