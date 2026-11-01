---
unique_name: basketball_c
name: Basketball_c
suggestion: 'No'
decision_markers:
- Data Quality Issue
original_source: Kaggle
year: '?'
required_split:
- Random (IID)
source_links:
- https://www.kaggle.com/datasets/yakhyojon/national-basketball-association-nba
type_adapter_id: curation-record-v1
---

## Comments

Imported from the TabArena curation workbook.

TabArena curation verdict: None-dataquality.

data from coursera, target is to predict whether a basketball player will last in the league for >=5 years. There is an OpenML version: Performance-Prediction

Potential issue: Unclear source, wrong data, see Kaggle discussions

Lennart: Data problems and missing source information, see Kaggle discussion

Andrej: Data quality issues

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nba_rookie_five_year_career` (TBD -> 2nd Tier, priority 1). Each is screened in its own record; this record's verdict stays the curator's.

## Reference

https://www.kaggle.com/datasets/yakhyojon/national-basketball-association-nba
