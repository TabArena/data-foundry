---
unique_name: delays_zurich_transport
name: delays_zurich_transport
checked_by:
- Andrej
data_foundry_status:
- 'DF: Suspended'
suggestion: TBD -> Yes
decision_markers:
- Time-series (Regression)
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
original_source: Github
year: '2017'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/d/40753
notebook_path: datasets/_maintenance/_suspended/delays_zurich_transport/delays_zurich_transport.ipynb
source_row: 620
type_adapter_id: curation-record-v1
---

## Comments

CC: ">5M samples delay data. Requires temporal split and/or time-invariant feature engineering."

Seems like the data originates from a 2016 Open Data Day Zurich project: https://github.com/OpenDataDayZurich2016/ODDPredictDelays?tab=readme-ov-file

Could likely get much more data like this by crawling the Zurich data website (https://www.stadt-zuerich.ch/opendata)

Contains weather features which leak. The sample rate is minutes, but the weather data is aggregated over days

Could certainly be framed as a tabular data task, but requires work

## Reference

@misc{seibold2017delayszurichtransport,
    author       = {Heidi Seibold},
    title        = {delays\_zurich\_transport},
    year         = {2017},
    month        = jun,
    howpublished = {OpenML dataset 40753},
    note         = {Uploaded 2017-06-01},
    url          = {https://www.openml.org/d/40753}
    }
