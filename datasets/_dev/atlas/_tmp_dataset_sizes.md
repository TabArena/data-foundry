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


New datasets brain dump, first col is sheet name currently:
* "USA Airport Dataset", 3.5M+ maybe, unclear preprocessing and target  (https://www.kaggle.com/datasets/flashgordon/usa-airport-dataset
)