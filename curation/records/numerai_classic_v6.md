---
unique_name: numerai_classic_v6
name: Numerai Classic v6.0 (Unity)
original_source: Company
year: '2026'
domain: finance
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://blog.numer.ai/unifying-numerai-and-signals
- https://forum.numer.ai/t/8367
- https://docs.numer.ai/numerai-tournament/data
needs_review:
- suggestion
type_adapter_id: curation-record-v1
---

## Comments

Created on 2026-10-26 at Lennart's ask (numerai_v5_2 issue 7): "Create the v6 data record, keep v5.2 as a frozen release". Not screened yet.

CC (2026-10-26, Lennart): create the v6 data record; numerai_v5_2 stays as a frozen release.

**Note (AI, 2026-10-26):** facts gathered for screening (records_research run of 2026-10-26):
- Release: data on 2026-10-16; v6 submissions from 2026-11-06; Signals merges into the tournament on 2027-01-01. The blog: "every row in Numerai's dataset was an anonymous stock ... Starting today, you do."
- Files (API snapshot 20261023): train.parquet 2,176,229,215 bytes (4,329,443 rows, 835 weekly Fridays 2003-01-03 to 2018-12-28), validation.parquet 1,396,219,377 bytes (2,717,738 rows, 407 Fridays 2019-01-04 to 2026-10-16; 85,490 rows of the last 12 dates without a target), features.json, and neutralizer files (300 columns per ticker and date).
- Stocks: 18,960 tickers in 47 countries (US 41% of rows, JP 15%); id columns `numerai_ticker`, `date`, `data_type`, and `composite_figi` (63% filled in validation).
- Features: 1,040, none shared with v5: 1,017 binned int8 features in 8 groups, 22 Signals numeric features with missing values, and `feature_country` (text). Sets: small 101, medium 351, all 1,040, signals 23.
- Targets: 24; `target` is an alias of `target_jupiter_60` (a 60-business-day return, five bins with shares 5/20/50/20/5%). Payouts from 2026-11-06 on NCORR and NMMC (correlation after neutralising with the Signals giant neutralizer, against the Jupiter 60D target); per-date CORR on target_jupiter_60 is computable without the neutralizer.
- Licence: Numerai's terms of service (4.2): tournament use only, no redistribution; only a definition could ship.
- Screening questions: real tickers, weekly dates and stock histories (median 218 weeks per ticker) now ship, and Numerai's own table marks "Time-series forecasting": the forecasting-scope test (SEL-10, TP-10) and the series question must be answered; the split by date and a gap for the 60-day target (12 weekly eras) as for v5.2.
