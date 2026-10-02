---
unique_name: sf_permit_time
name: sf_permit_time
checked_by:
- Lennart
- Alex
- Mustafa
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
- Free Text (Sentences)
collections:
- TexTabBench
original_source: GOV Website
year: '2018'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/aparnashastry/building-permit-applications-data
- https://data.sf.gov/Housing-and-Buildings/Building-Permits/i98e-djp9/about_data
notebook_path: datasets/beyond_iid/temporal/sf_permit_time/sf_permit_time.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/sf_permit_time/dataset.py
source_row: 737
type_adapter_id: curation-record-v1
---

## Comments

building permits
AP: might need spatial/temporal split

Likely preprocess and filter on permit type, and status. Revised cost and some other features might be leaking if the permit was granted or not and if it was granted might leak time to grant. A lot of spatial features, record id is also time informative

the description column: it seems to be diverse enough to be considered free text

LP: very borderline. We need to create some features or filter to meaningful descriptions as many are clearly just a category. Others include a reference to other permits, so there might also be leakage. needs some time to look at and work with.

CC (2026-10-01, Lennart): Leak audit: right-censored target fixed. The download (2026-02-05) only holds permits issued by then, so recent filings miss their slow permits: still-open share by filed year 1.8-5.3% (2015-21), 10.2% (2023), 11.1% (2024), 21.5% (2025), and the p90 of days to issue falls from about 300 days to 147 (2024) and 97 (2025). The v2 definition now keeps permits filed before 2024 (116,954 -> 99,847 rows) and uses 9 half-year test windows (2019-H2 to 2023-H2, train >= 55%, test 3,758-6,878 rows, horizon 6 months) instead of 6 yearly windows up to 2025. A newer download was considered and not taken: the October 2026 portal data showed 2024 and 2025 still filling in (2025 p90 97 -> 160 days; 954 more 2025 permits issued) while 2023 had nearly settled (216 -> 222), so it would only move the safe cut a few months. Revisit in a year or two. Also fixed: latitude and longitude were swapped (Location is WKT POINT (lon lat)); the download description now names the actual filter (filed_date 2015-2025; the old query link filtered on approved_date) and the portal's new domain data.sf.gov. The target is log(days to issue).
