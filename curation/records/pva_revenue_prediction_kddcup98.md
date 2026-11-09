---
unique_name: pva_revenue_prediction_kddcup98
name: KDD98
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Larger IID Data
collections:
- TabArena Reject
- TabSTAR
original_source: Website
year: '1998'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/d/42343
- https://kdd.ics.uci.edu/databases/kddcup98/kddcup98.html
notebook_path: datasets/beyond_iid/new_iid/pva_revenue_prediction_kddcup98/pva_revenue_prediction_kddcup98_clf.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/pva_revenue_prediction_kddcup98/dataset.py
source_row: 647
type_adapter_id: curation-record-v1
---

## Comments

CC: "Predict whether there was a response to mailing. Side story: A friend of mine used to work for a company whose customers were mainly old people still ordering stuff from physical catalogues. Predicting the response to direct mailing was one the tasks he worked on. So this good old task is still relevant :) ... In Germany? :D"

This could also be used as a classification task given the first dependent variable

The problem type is not a property of this dataset: it is *either* regression on the donation
amount *or* binary classification on whether the mailing got a response — one target or the
other, never both at once. After investigation we shipped the classification version, so
`problem_type` records `Binary Classification` and the curated dataset comes from
`pva_revenue_prediction_kddcup98_clf.ipynb`, not from the regression notebook next to it.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: stand_in roc_auc — the KDD Cup 98 net revenue of the mailing (sum of TARGET_D - $0.68 over mailed donors) needs the donation amount, which our binary-response task drops (cup98doc.txt).

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 6 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `SOLP3`, `SOLIH`, `RFA_2F`, `RFA_2A`, `GEOCODE2`, `DOMAIN_ses` (the README lists their levels); left unordered: `MDMAUD_recency` (a level outside the scale is a state of its own); `MDMAUD_frequency` (a level outside the scale is a state of its own); `MDMAUD_amount` (a level outside the scale is a state of its own); ordinal scales shipped as numbers, left as numbers for the curator's review: `INCOME`, `WEALTH1`, `WEALTH2`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 3 ordinal scales shipped as numbers are ordered categories (point 3); 3 columns with a state outside the scale ordered, the state placed by the rule.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `springleaf_marketing_response` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 5 coded columns carry their words; 3 scores are numbers (INCOME, WEALTH1, WEALTH2); DOMAIN_ses read row by row in the dictionary's two schemes (urban codes 2 and 3 were misread); AGEFLAG blank and GENDER A, C and Unknown missing.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

CC (2026-11-05, Lennart): GitHub issue #48 review: `DOMAIN_urbanicity` stays an unordered category with a note: the dictionary calls `DOMAIN` nominal and gives no density order of City and Suburban. The declared metric is checked.

## Review

**Outcome:** added. In the working copy since the migration; GitHub issue #48 (a column-type review of #37) proposes
ordering `DOMAIN_urbanicity`. The AI recommends keeping it unordered and adding the note the rule asks for.

**Main points:** Keep the neighbourhood's urbanicity unordered, with a note, or order it?

**Issues for Lennart:**

1. **Keep `DOMAIN_urbanicity` unordered, with a note on why?**

   * **Problem:**
     - `DOMAIN_urbanicity` (Urban, City, Suburban, Town, Rural, the first byte of `DOMAIN`) ships as an unordered category, and the notes do not say why.
     - Issue #48 proposes Rural < Town < Suburban < City < Urban, with low confidence: it did not check City against Suburban.
   * **Background:** The dictionary lists the levels U, C, S, T, R and calls `DOMAIN` "A nominal or symbolic field" ([cup98dic.txt](https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/cup98dic.txt)); it does not say whether a city neighbourhood is denser than a suburb[^1].
   * **Effect on the task:** Five levels in 191,769 rows; ordered or not, a model sees each level, so the choice changes little beyond the documented state.
   * **Consistency:** The second byte, `DOMAIN_ses`, is ordered because the dictionary names each level in words on one line.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Unordered, no note (implemented) | as now | none found | the rule asks for a note when the order stays unclear |
     | B | Unordered, with a note | one bullet in `curation_comments` | the source calls it nominal and gives no density order | a model cannot use that rural and urban are the two ends |
     | C | Ordered, Rural < Town < Suburban < City < Urban | `FeatureTypes(ordinal=...)` | the ends are clear; the dictionary's listing order read backwards | the City-Suburban step is a guess |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** on B, add a dated bullet to `curation_comments`: the dictionary lists U, C, S, T, R and calls
   the field nominal, the density order of City and Suburban is not given, so the column stays unordered (CLEAN-14).
   On C, add it to `ORDINAL_LEVELS` and remove it from `categorical`. Then `dataset check`, a CHANGELOG entry and a CC
   line in the record. Issue #48's `WEEKDAY_APPR_PROCESS_START` point (home_credit_default_risk) is not raised: the
   curator's rule of 2026-11-01 orders a named cycle from Monday with the wrap not shown.

   **Lennart (2026-11-05, change):** Option B: Unordered, with a note.

   **Resolved (2026-11-05, Lennart):** B. `DOMAIN_urbanicity` stays unordered; `curation_comments` say why.

   [^1]: **CLEAN-14** (Should): an order still unclear after the sources are checked stays unordered, with a note.

## Reference

Website / readme
