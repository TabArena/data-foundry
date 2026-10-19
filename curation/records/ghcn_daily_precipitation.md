---
unique_name: ghcn_daily_precipitation
name: GHCN-Daily precipitation (NOAA NCEI Global Historical Climatology Network - Daily, PRCP)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
- No Good Target (yet)
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: GOV Website
year: '2012'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.ncei.noaa.gov/pub/data/ghcn/daily/
- https://www.ncei.noaa.gov/pub/data/ghcn/daily/readme.txt
- https://doi.org/10.7289/V5D21VHZ
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

NOAA NCEI's archive of daily station observations: 133,039 stations in `ghcnd-stations.txt`, one fixed-width `.dly`
file per station with one row per station, element and month and 31 day slots (3.8 GB for all stations). It is an
observation archive without a prediction task. Any target built from it, such as tomorrow's rain at a station,
forecasts the station's own series, which the guidelines exclude. The curated sibling whose source defines the task
is `rain_in_australia`.

Zero mechanism: dry days, but the archive also stores trace precipitation as 0 with MFLAG "T" and has a "P" flag for
"missing presumed zero" (readme). Measured on one station only (USW00094728, Central Park, 57,632 observed days,
1869-2026): 66.7% of days are exactly 0, and 8.5% of all days are trace zeros. How common the "presumed zero" flag is
across the archive was not measured. Use terms: cite Menne et al. (2012) and the version DOI; no restriction stated.

## Reference

Menne M.J., Durre I., Vose R.S., Gleason B.E., Houston T.G. (2012). An overview of the Global Historical
Climatology Network-Daily database. Journal of Atmospheric and Oceanic Technology 29(7):897-910.
doi:10.1175/JTECH-D-11-00103.1. Dataset doi:10.7289/V5D21VHZ.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 7 (NOAA GHCN-D precipitation).
