---
unique_name: analcatdata_supreme
name: analcatdata_supreme
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
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
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/d/728
- https://www.openml.org/search?type=data&id=504&sort=runs&status=active
v2_path: datasets/_dev/tabarena-v0pt2/analcatdata_supreme/dataset.py
source_row: 718
type_adapter_id: curation-record-v1
---

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

**Assessment (AI, 2026-10-07):** OpenML 504/728/44040 and KEEL use `Log exposure` as the target; the response is the number of actions (original: Simonoff's book page). `Log exposure` leaks: it is shortened when Congress overturned a decision, and all 31 decisions whose exposure contradicts their year by 2+ years, or exceeds it, have an action; the definition uses the year-implied exposure. A temporal split cannot be built validly: every label counts actions in the same 1979-1988 window, known only at its end, and newer decisions have shorter exposures than any training decision. Implemented: IID 3x3, as the book models all decisions together. Small signal on 9/9 folds (LightGBM +0.021, hurdle +0.022; "any action" AUC 0.70, year alone 0.68). Alternative: No.

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
