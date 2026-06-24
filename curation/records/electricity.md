---
unique_name: electricity
name: electricity
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Forecasting)
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
original_source: OpenML
year: '1998'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/d/151
- https://www.kaggle.com/datasets/yashsharan/the-elec2-dataset
- https://www.openml.org/search?type=data&id=44156
- https://search.r-project.org/CRAN/refmans/dynaTree/html/elec2.html
source_row: 614
type_adapter_id: curation-record-v1
---

## Comments

CC: "leak if not temporal split; manually normalized but unclear how; day-wise and week-wise temporal connections"

Seems like valid/borderline forecasting as classification task with more side information

Paper talks a lot about the data https://cgi.cse.unsw.edu.au/~reports/papers/9905.pdf

"An appealing property of this dataset is that it is expected to contain drifting data distributions since, during the recording period, the electricity market was expanded to include adjacent areas. This allowed for the production surplus of one region to be sold in the adjacent region, which in turn dampened price levels."

R version is without missing values and only 27552 data points?

## Reference

@article{harries1999splice,
  title={Splice-2 comparative evaluation: Electricity pricing},
  author={Harries, Michael and Wales, New South and others},
  year={1999},
  publisher={University of New South Wales, School of Computer Science and Engineering~…}
}
