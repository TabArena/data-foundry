---
unique_name: perth_house_prices
name: Perth-House-Prices
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 1
tags:
- Non-IID (Temporal)
collections:
- TabSTAR
original_source: Kaggle
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://www.openml.org/search?type=data&id=43822&sort=runs&status=active
- http://house.speakingsame.com/
- https://www.kaggle.com/datasets/syuzai/perth-house-prices
v2_path: datasets/_dev/tabarena-v0pt2/perth_house_prices/dataset.py
source_row: 729
type_adapter_id: curation-record-v1
---

## Comments

Data looks real, way back machine shows this was once a real website. Should be usable for some sort of house price prediction task

Data looks good to use; again, house prices...
But otherwise great features and setup for one of these tasks

Some scraping and minor issues: https://www.kaggle.com/datasets/syuzai/perth-house-prices/discussion/383033

**Assessment (AI, 2026-10-07):** Provenance traced: the uploader scraped house.speakingsame.com and added G-NAF coordinates and bettereducation ranks; OpenML 43822 is the same table. Each property appears once, with its latest sale before 31 January 2021; each suburb holds only its newest sales. The upload stops at $2,440,000, an undocumented cut (1.5% of 2015-2020 house sales in a 2024 Kaggle scrape cost more): the dearest suburbs keep only cheaper sales. The attributes are the site's record: 563 sales predate the build year (dropped), and 23% of the 2020 sales shared with that scrape list fewer bedrooms or bathrooms than their sold listing (stale; noise, not a leak). Temporal task, 9 monthly windows of 2020; LightGBM R² 0.86, no probe flags.

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source -, shape +, risk - (Issue 1: target capped at $2.44M, missing sales unrecoverable; issue 2 stale test-period records). Temporal house-price regression with rich features, but a capped target and stale records weaken it in a crowded domain.

**Assessment (AI, 2026-10-20):** review panel (full, re-check): ship after changes, applied in the definition. Fit `approximate` under USE-8 as written (truncated at $2.44M with dearer sales absent, attributes as of the January 2021 scrape, the school rank kept as a weak potential leak); 147 station and 58 school values from before the opening blanked (LEAK-10); the 563 pre-build sales dropped as land or off-the-plan sales (USE-7), the 140 build-year sales kept; 19 floor areas and 2 bathroom counts that are impossible set to missing; `Vic` split into Victoria Street and Victoria Park. LightGBM skill 0.862 over the dummy, no probe flag. For the curator (REVIEW.md issues 1, 7, 6, 3, 5): the fit label (house-family USE-8 item), a one-month gap or no gap (house_prices_nominal issue 4), spaced monthly windows (`step=3`) or contiguous 2020 windows with an exception, the history from 1988 or 2013, a `UNIT` flag. heptix/perth-property-prices (property type, exact dates, no truncation) stays a separate candidate. Priority 1: gap -, use case -, source -, shape +, risk - (use case written by the curation and fit approximate; a Kaggle scrape with no first publication; the truncation cannot be repaired from this source and a weak potential leak is kept).

CC (2026-10-21, Lennart): ok on the follow-up item: a strong kept leak does not make the fit approximate (USE-8 amended); the kept leak is named in `fit_reason` as kept, not as a gap.

**Assessment (AI, 2026-10-21):** fit stays `approximate` for the truncation at $2.44M and the attributes as of the January 2021 scrape; the school rank left `fit_reason` (its potential-leak note stays); REVIEW.md issue 1 settled and removed.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Kaggle dataset of scraped listings; the source defines no task or metric (rmse on the log price).

**Assessment (AI, 2026-10-21):** metric now `Metric.from_context("rmsle", target_transform="log")` instead of the fallback rmse on the log target: a sale price's error matters relative to the price; the target still ships as log, and RMSLE is computed after the inverse, on the original scale (MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).
