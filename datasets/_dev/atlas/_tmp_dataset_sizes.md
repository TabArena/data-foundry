# Atlas — Dataset tracker (TEMP)

Data curation for a benchmark from 1M to 10M training samples.

**11 datasets** from BeyondArena:

| Dataset | Rows (full ≈) | Cols | Category | ≥10M rows | Subsampled to 1M in BeyondArena |
|---|---:|---:|---|:---:|:-------------------------------:|
| `delivery_eta` | 17,044,043 | 227 | temporal | ✅ |                ✅                |
| `climate_model_weather_forecasting` | 16,951,828 | 104 | temporal | ✅ |                ✅                |
| `maps_router_eta` | 13,639,272 | 989 | temporal | ✅ |                ✅                |
| `consumer_complaints` | 13,184,632 | 18 | temporal | ✅ |                ✅                |
| `cooking_time` | 12,799,642 | 197 | temporal | ✅ |                ✅                |
| `amex_non_iid` | 5,531,451 | 190 | grouped |  |                ✅                |
| `lending_club` | 2,260,701 | 151 | temporal |  |                ✅                |
| `sepsis_prediction` | 1,552,210 | 44 | grouped |  |                ✅                |
| `home_credit_default_stability` | 1,526,659 | 719 | temporal |  |                ✅                |
| `mercari_price_suggestion` | 1,482,535 | 8 | new_iid |  |                ✅                |
| `electric_motor_temperature_prediction` | 1,330,816 | 13 | grouped |  |      — (kept full already)      |



## New candidates

Sorted by **best-estimate usable rows** (post-preprocessing where known; raw used as proxy when unknown).
**Viability** is judged from the notes against the 1M–10M usable-rows target:
🟢 most likely · 🟡 needs more work · 🔴 very unlikely.

| Dataset | Rows raw ≈ | Rows usable ≈ | Category | Viability | Concern / status                                                               |
|---|---:|---:|---|:---:|--------------------------------------------------------------------------------|
| [G-Research Crypto Forecasting](https://www.kaggle.com/competitions/g-research-crypto-forecasting/data?select=train.csv) | ~24M | ~24M | temporal | 🟢 | Usable, but problems from anonymization                                        |
| [KASANDR](https://archive.ics.uci.edu/dataset/385/kasandr) | ~17.8M | ~17.8M | grouped/temporal | 🔴 | RecSys task, not naturally tabular (15.84M train + 1.92M test)                 |
| [CSE-CIC-IDS2018](https://www.kaggle.com/datasets/bcccdatasets/large-scale-ids-dataset-bccc-cse-cic-ids2018/) | ~46M | ~16.2M | temporal | 🟡 | Lots of noise / simulated traffic                                              |
| [UCI HIGGS](https://www.openml.org/d/42769) | ~11M | ~11M | IID | 🟡 | Bias from simulation                                                           |
| [US Accidents](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) | ~7.7M | ? | temporal | 🔴 | Unclear predictive task, more of a data dump                                   |
| [PeopleDataLabs 7M company](https://www.kaggle.com/datasets/peopledatalabssf/free-7-million-company-dataset) | ~7.17M | ? | temporal | 🔴 | Unclear predictive task, more of a data dump                                   |
| [Yelp Open Dataset](https://business.yelp.com/data/resources/open-dataset/) | ~6.99M | ? | temporal | 🔴 | Unclear task, most likely RecSys (review.json)                                 |
| [KDD Cup 1999](https://www.openml.org/d/42746) | ~4.9M | ~4.9M | temporal* | 🟢 | Temporal data but no usable time index                                         |
| [CARE to Compare Wind SCADA](https://zenodo.org/records/15846963) | ~4.7M | ? | grouped/temporal | 🟡 | Needs proper setup to determine real size and task                             |
| [CHAMPS Scalar Coupling](https://www.kaggle.com/competitions/champs-scalar-coupling/data?select=train.csv) | ~4.66M | ? | grouped (molecule) | 🟡 | Unclear if a tabular task                                                      |
| [STEG Electricity & Gas Fraud](https://zindi.africa/competitions/fraud-detection-in-electricity-and-gas-consumption-issea/) | ~4.48M | ~4.48M | grouped/temporal | 🟡 | Need to investigate data                                                                              |
| [Avito Prohibited Content](https://www.kaggle.com/competitions/avito-prohibited-content/data?select=avito_train.zip) | ~4M+ | ? | IID/temporal | 🟡 | Needs a lot of preprocessing, unclear final size                               |
| [USA Airport Dataset](https://www.kaggle.com/datasets/flashgordon/usa-airport-dataset) | ~3.5M+ | ? | temporal | 🟡 | Unclear preprocessing and target                                               |
| [Numerai Tournament Data](https://github.com/numerai/example-scripts/tree/master/numerai) | ~2.4M+ | ~2.4M | temporal | 🟡 | Needs a lot of care; older 2016 Kaggle set only ~100K                          |
| [Expresso Churn](https://zindi.africa/competitions/expresso-churn-prediction/data) | ~2.15M | ? | temporal/IID | 🟡 | Need to investigate data                                                       |
| [NYC TLC (trip-duration subset)](https://www.kaggle.com/c/nyc-taxi-trip-duration) | ~1.46M | ~1.46M | temporal | 🟡 | Subset of billions of NYC trips; unclear/no predictive task                    |
| [TableShift Diabetes / BRFSS](https://tableshift.org/datasets.html#diabetes) | 1,444,176 | ~1.44M | IID/temporal/grouped | 🟡 | No predictive task defined                                                     |
| [FORCE 2020 Well-Log Lithology](https://zenodo.org/records/4351156) | ~1.17M | ~1.17M | grouped | 🟡 | Needs domain deep dive (train.csv)                                             |
| [Azubian Customer Churn](https://zindi.africa/competitions/customer-churn-prediction-challenge-for-azubian) | ~1.08M | ? | ? | 🟡 | Needs investigation                                                            |
| [Rosbank Churn](https://huggingface.co/datasets/pytorch-lifestream/rosbank-churn) | ~1M | ? | temporal | 🟡 | Transaction-level; data needs investigation                                    |
| [Acquire Valued Shoppers](https://www.kaggle.com/c/acquire-valued-shoppers-challenge) | ~350M | ~150K | grouped/temporal | 🔴 | Collapses to ~150K after correct preprocessing; unclear if setting makes sense |
| [iSDAsoil](https://www.isda-africa.com/isdasoil/open-soil-data/) | >>1M (grid) | ~130K | grouped/temporal | 🔴 | Labeled input samples only ~130K; unclear final state                          |
| [Zillow Prize](https://www.kaggle.com/competitions/zillow-prize-1) | ~2.99M | ~90K | temporal | 🔴 | properties_2016 ~2.99M but labeled train_2016 only ~90K                        |
| [Alfa Battle 2.0](https://www.kaggle.com/datasets/mrmorj/alfabattle-20) | multi-M | ? | grouped/temporal | 🟡 | Transactional event log; sample count unconfirmed                              |
| [Sasol Customer Retention](https://zindi.africa/competitions/sasol-customer-retention-recruitment-competition/data) | multi-M | ? | temporal | 🟡 | Exact count and task unconfirmed                                               |
