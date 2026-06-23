---
unique_name: analcatdata_supreme
name: analcatdata_supreme
checked_by:
- Lennart
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
original_source: Other
year: '2003'
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: TBD
original_data_state: One Table
source_links:
- https://www.openml.org/d/728
- https://www.openml.org/search?type=data&id=504&sort=runs&status=active
source_row: 718
type_adapter_id: curation-record-v1
---

# analcatdata_supreme

## Comments

CC: ""Actual task is regression; ""1[data from] between 1953 and 1988 that fell under Judiciary Committee jurisdiction during the 96th through 101st
Congress, 1979-1988""

"We will attempt to stochastically model such action using the
4052 Supreme Court decisions handed down between 1953 and 1988 that
fell under Judiciary Committee jurisdiction during the 96th through 101st
Congress, 1979-1988 (Zorn, 1998, with data given in the file supreme)."
From the book, dataset from Chris Zorn -> real source https://journals.sagepub.com/doi/abs/10.1177/0049124198026003004

". Since some cases were handed down after 1979,
and in some cases Congress overturned a decision before 1988, not all cases
were "available" for action for the entire 10-year period, so the logarithm
of the number of years of "exposure" is also included (expected, therefore,
to be directly related to the number of actions taken)."

Correct target seems to be regression number of actions taken. We could overrule to clf as well""

## Reference

@article{zorn1998analytic,
  title={An analytic and empirical examination of zero-inflated and hurdle Poisson specifications},
  author={Zorn, Christopher JW},
  journal={Sociological Methods \& Research},
  volume={26},
  number={3},
  pages={368--400},
  year={1998},
  publisher={SAGE PERIODICALS PRESS}
}
