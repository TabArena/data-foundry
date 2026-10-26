---
unique_name: zillow_prize
name: Zillow Prize
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- Review Prio 1 (Atlas)
collections:
- New (BeyondArena)
original_source: Kaggle
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://www.kaggle.com/competitions/zillow-prize-1
v2_path: datasets/_dev/tabarena-v0pt2/zillow_prize/dataset.py
source_row: 727
type_adapter_id: curation-record-v1
---

## Comments

Looks like a good temporal dataset

Multiple targets due to working for multiple time horizons, still looks good to just take one of these that we can reproduce on train data as it computes the score in a special way based on these forecasts

Not a lot of information about solutions. Some I see use extensive feature engineering. See what / how we can give it to the model most raw

Basic: https://www.kaggle.com/code/anokas/simple-xgboost-starter-0-0655

**Assessment (AI, 2026-10-07):** Valid temporal regression. The target is Zillow's own residual, log(Zestimate) - log(SalePrice), which Zillow models to improve the Zestimate (FAQ, discussion 33899). Each sale must take the property file of its year: properties_2017 holds edits made after early-2016 sales (building facts differ for 1.2-2.0% of parcels sold January-May 2016, 0.81% of unsold ones), and Zillow warns about its tax values (discussion 40408). August and September 2017 are incomplete ("a biased sample", same post). Concern: sales with |logerror| > 1 (0.4%, mostly miskeyed prices) hold half of the squared error; the competition scored MAE. The signal is small but real: robust LightGBM fits beat the train mean on 9 of 9 monthly windows. The rules forbid redistribution.

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap -, use case +, source +, shape +, risk - (Issue 2: probes flag no_signal, drift_baseline, unstable; target dominated by miskeyed-price outliers). Real company task with a clear use case and documented data, but the signal is tiny and may not separate methods.

**Assessment (AI, 2026-10-20):** review panel (full tier): ship after changes. The fit is `approximate` (USE-6, USE-8): the Zestimate, the listing data and the last sale price were never released. The tax delinquency is one snapshot of about September 2016 in both property files, after the sales of January to August 2016 (1.5% flagged against 3.8% from September 2016), so the definition blanks it for those sales (LEAK-10 via LEAK-7); blanking, keeping or dropping it give the same L1 LightGBM skill within the seed spread. Building facts differ between the files for 1.4-2.3% of the parcels sold January to May 2016 and 3.2-3.7% of the parcels sold only in 2017, flat by sale month; the tax values show no reset at the sale (LEAK-10's "did not change" clause). Signal: untuned LightGBM with an absolute-error loss beats the train mean in 8 or 9 of 9 windows (R^2 about 0.001-0.012), squared-error fits in 3 or 4; the train median loses to the mean in 9 of 9, so the gain is in the features (TP-2). TP-1: tuned results pending; if tuned methods do not beat the dummy window by window, `TBD -> 2nd Tier`. 0.38% of the rows hold half of the squared error; RMSE or MAE is open in the working copy's TP-6 item. The prediction point rests on Kaggle's FAQ, which no one could read (REVIEW.md issue 3). Priority 2: gap -, use case -, source +, shape +, risk - (fit approximate; small signal and an RMSE dominated by miskeyed prices; the blind reviewer would exclude).

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric set to `mae`, the competition's metric (was the default RMSE); 0.38% of the rows hold 49.9% of the squared error. Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ok on the follow-up item: a strong kept leak does not make the fit approximate (USE-8 amended); the kept leak is named in `fit_reason` as kept, not as a gap.

**Assessment (AI, 2026-10-21):** fit stays `approximate` for the inputs Zillow never released; the facts that may postdate the sale left `fit_reason` (the split text still names them).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: the presence flags hashottuborspa, fireplaceflag, poolcnt, pooltypeid10, pooltypeid2, pooltypeid7, decktypeid, storytypeid (booleans) and taxdelinquencyflag (1.0 / 0.0).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source mae — MAE of logerror on the Zillow Prize evaluation page.

CC (2026-10-26, Lennart): issue 3: the competition's Data page and discussions read; the prediction point is confirmed by Zillow's FAQ (Andrew Martin, discussion 33899: the Zestimate "from the first day of the month in which they were sold").

CC (2026-10-26, Lennart): issue 6: "Can you fix this? what was done in the competition to handle this error?": the competitors kept the raw codes and Zillow published no conversion; the definition maps the 2017 codes onto the 2016 scale, confirmed on all 1.94M parcels by the crosstab in discussion 40453, recorded as an exception to CLEAN-21, and the column becomes categorical.

CC (2026-10-26, Lennart): issue 9: "make it categorical, but also please check what top solution did ... would this not be multiple cat columns maybe?": one categorical `census_tract` (11-digit tract ID, 3,030 levels); both census tract-and-block columns dropped (county = fips; block group and block near-identifiers).

**Exception to CLEAN-21 (2026-10-26, Lennart):** `buildingqualitytypeid` of properties_2017 is mapped onto the 2016 scale with the map the data shows (each 2017 code from one 2016 code), with no conversion published by Zillow; the fact that sets it apart: the crosstab of all 1.94M parcels with a code in both files (discussion 40453) confirms the map. Serves P7: one meaning per code in the training and the test rows.

**Assessment (AI, 2026-10-26):** applied; `dataset check` clean (153,108 rows, 56 columns). The research (Meta Kaggle's 2,813 public forum messages, the 19 most-voted kernels) found no public top-3 write-up. No open issue is left, so the folder's REVIEW.md is removed.

CC (2026-10-26, Lennart): verdict ship.
